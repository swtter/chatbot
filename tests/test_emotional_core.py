from emotional_core import build_system_prompt, update_emotion, update_memory

def test_vulnerability_increases_warmth_and_trust():
    state=update_emotion({"warmth":50,"trust":40,"longing":20,"mood":"好奇"},"最近压力很大，也有点孤独")
    assert state["warmth"]>50 and state["trust"]>40 and state["mood"]=="心疼"

def test_memory_replaces_fact_by_category():
    memory=update_memory([],"我叫小夏，我喜欢深夜散步"); memory=update_memory(memory,"其实我喜欢雨天看电影")
    assert "称呼：小夏" in memory and "喜欢：雨天看电影" in memory
    assert len([fact for fact in memory if fact.startswith("喜欢：")])==1

def test_prompt_contains_persona_state_memory_and_boundary():
    prompt=build_system_prompt({"name":"晚风","style":"温柔","tone":"暧昧"},{"warmth":60,"trust":50,"longing":10,"mood":"温柔"},["称呼：小夏"])
    assert all(term in prompt for term in ("晚风","小夏","暧昧","不得生成露骨色情描写"))
