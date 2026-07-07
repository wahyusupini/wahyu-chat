import streamlit as st
from google import genai
if "genai_client" not in st.session_state:
 st.session_state.genai_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# Konfigurasi Halaman
st.title("Gemini Chatbot")
st.caption("Chatbot sederhana menggunakan Google Gemini")

# Sidebar: Pengaturan App
with st.sidebar:
    st.subheader("Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password")
    reset_button = st.button("Reset Percakapan")

if not google_api_key:
    st.info("Masukkan Google AI API Key di sidebar untuk memulai.")
    st.stop()

try:
    client = genai.Client(api_key=google_api_key)
except Exception as e:
    st.error(f"API Key tidak valid: {e}")
    st.stop()

if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ketik pesanmu di sini..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.chat.send_message(prompt)
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Terjadi error: {e}")
