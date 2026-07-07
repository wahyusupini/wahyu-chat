import streamlit as st
from google import genai

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini Chatbot", page_icon="💬", layout="centered")
st.title("💬 Gemini Chatbot")
st.caption("Chatbot simpel, stabil, dan anti-error")

# 2. Sidebar Pengaturan
with st.sidebar:
    st.subheader("Pengaturan")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    reset_button = st.button("Reset Percakapan")

# 3. Validasi API Key
if not google_api_key:
    st.info("🔑 Silakan masukkan Google AI API Key Anda di sidebar untuk memulai.")
    st.stop()

# 4. Simpan Riwayat Pesan dalam Bentuk Teks Biasa
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tombol Reset Percakapan
if reset_button:
    st.session_state.messages = []
    st.rerun()

# 5. Tampilkan Riwayat Obrolan di Layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Proses Input Pesan Baru dari User
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # Tampilkan dan simpan pesan user ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tampilkan respon dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Buat koneksi client yang selalu segar (anti 'client has been closed')
            client = genai.Client(api_key=google_api_key)

            # Gabungkan seluruh riwayat pesan agar Gemini ingat obrolan sebelumnya
            full_prompt = "Kamu adalah asisten AI yang ramah. Berikut adalah riwayat obrolan kita:\n"
            for msg in st.session_state.messages:
                full_prompt += f"{msg['role']}: {msg['content']}\n"
            full_prompt += "assistant: "

            # Panggil model utama 'gemini-2.5-flash' yang sudah pasti didukung
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
            )

            # Tampilkan hasil respon di layar browser
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"Terjadi kendala: {e}")
