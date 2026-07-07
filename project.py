import streamlit as st
from google import genai

st.title("AI Chatbot")

# 1. Simpan client di session_state agar tidak tertutup saat streamlit rerun
if 'client' not in st.session_state:
    st.session_state.client = genai.Client(api_key=st.secrets["AIzaSyCal0KCF0uoKXK0mEHZa4DYYdraBs8kyEY"])

# 2. Simpan chat session menggunakan client yang ada di session_state
if 'chat' not in st.session_state:
    config = {"system_instruction": "Anda adalah AI chatbot yang selalu merespon dan menjawab dalam bahasa Indonesia."}
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.5-flash",
        config=config
    )

# 3. Menampilkan riwayat pesan sebelumnya
for message in st.session_state.chat.get_history():
    role = "user" if message.role == "user" else "assistant"
    with st.chat_message(role):
        st.write(message.parts[0].text)

# 4. Input pesan baru dari pengguna
if prompt := st.chat_input("Ketik pesan Anda di sini..."):
    # Tampilkan pesan user di layar
    with st.chat_message("user"):
        st.write(prompt)

    # Kirim pesan menggunakan chat session yang tersimpan dan tampilkan respon
    response = st.session_state.chat.send_message(prompt)
    with st.chat_message("assistant"):
        st.write(response.text)