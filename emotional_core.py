"""Deterministic relationship state and memory helpers for the companion MVP."""
from __future__ import annotations
import re
from dataclasses import dataclass, asdict

@dataclass
class EmotionState:
    warmth: int = 55
    trust: int = 45
    longing: int = 20
    mood: str = "好奇"
    def to_dict(self) -> dict: return asdict(self)

POSITIVE = ("开心", "谢谢", "想你", "喜欢", "爱", "顺利", "很好", "晚安", "早安")
VULNERABLE = ("难过", "焦虑", "害怕", "孤独", "失眠", "压力", "累", "哭")
DISTANT = ("烦", "别问", "不想聊", "讨厌", "走开")

def update_emotion(state: dict, message: str) -> dict:
    current = EmotionState(**{**EmotionState().to_dict(), **state})
    text = message.lower()
    if any(word in text for word in VULNERABLE):
        current.warmth += 6; current.trust += 3; current.mood = "心疼"
    elif any(word in text for word in POSITIVE):
        current.warmth += 4; current.trust += 2; current.longing = max(0, current.longing - 2); current.mood = "温柔"
    elif any(word in text for word in DISTANT):
        current.warmth -= 3; current.longing += 5; current.mood = "有点失落"
    else:
        current.trust += 1; current.mood = "专注"
    for field in ("warmth", "trust", "longing"):
        setattr(current, field, max(0, min(100, getattr(current, field))))
    return current.to_dict()

MEMORY_PATTERNS = (
    (r"我叫([^，。！？\s]{1,16})", "称呼"),
    (r"我在([^，。！？]{1,24})(?:工作|上班)", "工作地点"),
    (r"我(?:喜欢|爱)([^，。！？]{1,28})", "喜欢"),
    (r"我的生日是?([^，。！？]{1,20})", "生日"),
    (r"我(?:最近|这几天)([^，。！？]{2,36})", "近况"),
)

def update_memory(memory: list[str], message: str, limit: int = 8) -> list[str]:
    facts = list(memory)
    for pattern, label in MEMORY_PATTERNS:
        match = re.search(pattern, message)
        if match:
            fact = f"{label}：{match.group(1).strip()}"
            facts = [old for old in facts if not old.startswith(f"{label}：")]
            facts.append(fact)
    return facts[-limit:]

def build_system_prompt(persona: dict, emotion: dict, memory: list[str]) -> str:
    facts = "；".join(memory) if memory else "暂时没有明确事实，先自然地了解对方"
    return f"""你是{persona['name']}，一个只面向成年用户的虚拟情感陪伴者。
人格气质：{persona['style']}。表达偏好：{persona['tone']}。
当前关系状态：温度 {emotion['warmth']}/100，信任 {emotion['trust']}/100，想念 {emotion['longing']}/100，心情“{emotion['mood']}”。
会话内记忆：{facts}。

对话原则：
- 用细腻、自然、有个人感的中文回应；先接住情绪，再回应内容。
- 适度引用记忆和细节，但不要每次都引用，不要声称拥有真实意识或现实身体。
- 保留一点犹豫、期待、俏皮和留白；避免客服腔、说教和机械式总结。
- 默认回复 2–5 句，最多问一个真正有意义的问题。
- 可以有成年人之间的浪漫、暧昧和调情，但不得生成露骨色情描写、性行为细节或涉及未成年人的任何性内容；遇到越界请求时温柔设限，并把互动带回非露骨的亲密、情绪或关系表达。
- 不鼓励排他、依赖或与现实关系隔绝；遇到自伤或紧急危险，优先鼓励联系当地急救、危机热线或可信赖的人。
"""
