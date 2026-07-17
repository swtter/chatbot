import os
import streamlit as st
from openai import OpenAI
from emotional_core import build_system_prompt, update_emotion, update_memory

st.set_page_config(page_title="晚风 · 情感陪伴", page_icon="🌙", layout="centered")
st.markdown("""<style>
.stApp{background:radial-gradient(circle at 20% 0%,#2a1d3f 0,#12101c 46%,#0b0a10 100%)}
[data-testid="stSidebar"]{background:#171321;border-right:1px solid #352944}.hero{padding:1.1rem 0 .5rem}.hero h1{margin:0;font-size:2.1rem;letter-spacing:-.04em}.hero p{color:#b9aec6;margin-top:.35rem}.status{display:inline-block;padding:.3rem .65rem;border:1px solid #59456f;border-radius:999px;color:#ddc9ef;font-size:.82rem;background:#251c31}[data-testid="stChatMessage"]{background:rgba(33,27,43,.78);border:1px solid #3b3048;border-radius:18px;padding:.8rem 1rem}.privacy{color:#8f859b;font-size:.78rem}
</style>""", unsafe_allow_html=True)
DEFAULT_EMOTION={"warmth":55,"trust":45,"longing":20,"mood":"好奇"}
for key,value in {"messages":[],"memory":[],"emotion":DEFAULT_EMOTION.copy()}.items():
    if key not in st.session_state: st.session_state[key]=value

with st.sidebar:
    st.header("塑造你的陪伴者")
    name=st.text_input("名字","晚风",max_chars=16)
    style=st.selectbox("人格",["温柔敏感，善于发现细节","俏皮自信，带一点若即若离","安静理性，不太擅长直白表达"])
    tone=st.select_slider("亲密表达",["克制","自然","亲昵","暧昧"],value="自然")
    model=st.selectbox("模型",["gpt-4o-mini","gpt-4.1-mini"],help="需由你的 API 账户支持")
    api_key=st.text_input("OpenAI API Key",value=os.getenv("OPENAI_API_KEY",""),type="password")
    st.caption("密钥只用于本次应用会话，不写入记忆。")
    st.divider(); emotion=st.session_state.emotion; st.subheader("此刻的关系"); st.caption(f"心情 · {emotion['mood']}")
    st.progress(emotion["warmth"]/100,text=f"温度 {emotion['warmth']}"); st.progress(emotion["trust"]/100,text=f"信任 {emotion['trust']}")
    with st.expander(f"会话记忆 · {len(st.session_state.memory)} 条"):
        if st.session_state.memory:
            for fact in st.session_state.memory: st.markdown(f"· {fact}")
        else: st.caption("她还在慢慢认识你。")
    if st.button("清空这次相遇",use_container_width=True):
        st.session_state.messages=[]; st.session_state.memory=[]; st.session_state.emotion=DEFAULT_EMOTION.copy(); st.rerun()

st.markdown(f'<div class="hero"><span class="status">● 在线 · {st.session_state.emotion["mood"]}</span><h1>{name}</h1><p>不急着回答。先好好听你说。</p></div>',unsafe_allow_html=True)
st.markdown('<p class="privacy">仅限成年人 · 可暧昧但不露骨 · 记忆只保留在当前浏览器会话</p>',unsafe_allow_html=True)
if not st.session_state.messages:
    with st.chat_message("assistant",avatar="🌙"): st.markdown("你来了。今天想让我安静地陪你一会儿，还是想说点一直没机会说的话？")
for message in st.session_state.messages:
    with st.chat_message(message["role"],avatar="🌙" if message["role"]=="assistant" else "🫧"): st.markdown(message["content"])
if prompt:=st.chat_input("跟她说点什么…",disabled=not api_key):
    st.session_state.messages.append({"role":"user","content":prompt}); st.session_state.memory=update_memory(st.session_state.memory,prompt); st.session_state.emotion=update_emotion(st.session_state.emotion,prompt)
    with st.chat_message("user",avatar="🫧"): st.markdown(prompt)
    try:
        stream=OpenAI(api_key=api_key).chat.completions.create(model=model,messages=[{"role":"system","content":build_system_prompt({"name":name,"style":style,"tone":tone},st.session_state.emotion,st.session_state.memory)},*st.session_state.messages[-16:]],temperature=.85,stream=True)
        with st.chat_message("assistant",avatar="🌙"): response=st.write_stream(stream)
        st.session_state.messages.append({"role":"assistant","content":response})
    except Exception: st.error("刚才的连接没有成功。请检查 API Key、模型权限或网络后再试。")
if not api_key: st.info("在左侧填入 OpenAI API Key 后，就可以开始对话。",icon="🔑")
