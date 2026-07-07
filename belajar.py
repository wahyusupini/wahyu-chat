import streamlit as st
from google import genai

# 1. Konfigurasi Halaman
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

# Tombol Reset
if reset_button:
    st.session_state.messages = []
    st.rerun()

# 5. Tampilkan Riwayat Obrolan di Layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 6. Proses Input Pesan Baru
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # Tampilkan dan simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tampilkan respon asisten
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            # Buat client yang selalu segar setiap kali tombol enter ditekan
            client = genai.Client(api_key=google_api_key)

            # Minta Gemini merespon langsung dengan membaca seluruh riwayat teks
            # Kita gabungkan riwayat menjadi satu kesatuan teks utuh (Prompt Injection History)
            full_prompt = "Kamu adalah asisten AI yang ramah. Berikut adalah riwayat obrolan kita:\n"
            for msg in st.session_state.messages:
                full_prompt += f"{msg['role']}: {msg['content']}\n"
            full_prompt += "assistant: "

            # Panggil API secara langsung (Cara ini 100% BEBAS dari error 'client has been closed')
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=full_prompt,
            )

            # Tampilkan hasil
            message_placeholder.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})

        except Exception as e:
            st.error(f"Terjadi kendala: {e}")
