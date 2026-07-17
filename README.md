# 🌙 晚风 — 情感陪伴聊天 MVP

基于 Streamlit 与 OpenAI API 的成年人情感陪伴原型。它不只是逐句问答：陪伴者会呈现细腻人格、随对话变化的简单情绪，并记住当前会话里用户主动分享的少量信息。

## 功能

- 三种人格气质与四档亲密表达，可在侧边栏即时调整
- 温度、信任、想念和当前心情组成的轻量情绪状态
- 提取称呼、喜好、生日、近况等会话内记忆（最多 8 条）
- 结合人格、情绪和记忆动态生成系统提示
- 流式回复、现代深色界面、最近 16 条消息上下文
- 成人向浪漫与暧昧，但明确禁止露骨色情及任何未成年人性内容
- 危机情形下优先引导用户联系现实支持

> 这是产品原型，不应被视为真人、心理治疗服务或紧急支持渠道。会话状态仅存在于当前 Streamlit 会话，刷新或清空后可能丢失。

## 本地运行

需要 Python 3.10+ 和自己的 OpenAI API Key。

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

在侧边栏输入 API Key，或在启动前设置 `OPENAI_API_KEY` 环境变量。请勿把密钥提交到仓库。

## 测试

```bash
pytest -q
python -m py_compile streamlit_app.py emotional_core.py
```

## 当前限制与下一步

当前记忆是规则提取且只在会话内保存，情绪状态也不是心理学模型。生产化前应增加账户与加密存储、可查看/删除的用户记忆、年龄门槛与同意流程、内容审核、危机响应、本地化隐私政策，以及完善的模型失败与限流处理。
