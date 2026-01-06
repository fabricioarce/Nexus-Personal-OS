import streamlit as st
from backend.app.core.rag_chat_engine_api import DiarioRAGChat

st.set_page_config(page_title="Diario Reflexivo", layout="centered")

st.title("🧠 Diario Reflexivo")

if "chat" not in st.session_state:
    st.session_state.chat = DiarioRAGChat()

pregunta = st.text_area("Escribe tu reflexión o pregunta:")

if st.button("Reflexionar"):
    if pregunta.strip():
        with st.spinner("Pensando..."):
            respuesta = st.session_state.chat.preguntar(pregunta)

        st.markdown("### 🤖 Respuesta")
        st.write(respuesta)
