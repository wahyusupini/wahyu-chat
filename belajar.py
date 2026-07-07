import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="centered")
st.title("💬 Gemini Chatbot")
st.caption("Chatbot sederhana menggunakan Google Gemini SDK terbaru")

# 2. Pembuatan Sidebar Pengaturan
with st.sidebar:
    st.subheader("Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda di sini...")
    reset_button = st.button("Reset Percakapan")

# 3. Validasi Keberadaan API Key
if not google_api_key:
    st.info("🔑 Silakan masukkan Google AI API Key Anda di menu sidebar untuk memulai percakapan.")
    st.stop()

# 4. Inisialisasi Google GenAI Client secara Aman
try:
    client = genai.Client(api_key=google_api_key)
except Exception as e:
    st.error(f"Inisialisasi gagal. Periksa kembali API Key Anda: {e}")
    st.stop()

# 5. Mengatur Sesi Chat & Riwayat Pesan di Session State
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Jika tombol reset ditekan, bersihkan riwayat chat
if reset_button:
    st.session_state.chat = client.chats.create(model="gemini-2.5-flash")
    st.session_state.messages = []
    st.rerun()

# 6. Menampilkan Riwayat Obrolan yang Sudah Ada
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Pemrosesan Input Chat Baru dari User
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # Tampilkan pesan user ke layar dan simpan ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Kirim pesan ke API Gemini dan terima responnya
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            response = st.session_state.chat.send_message(prompt)
            message_placeholder.markdown(response.text)
            # Simpan respon asisten ke riwayat
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Terjadi kendala saat memproses pesan: {e}")
