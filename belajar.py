import streamlit as st
from google import genai
from google.genai import types

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini Chatbot Pro", page_icon="💬", layout="centered")

# ==================== FITUR MENARIK: CUSTOM CSS BACKGROUND ====================
st.markdown("""
    <style>
    /* 1. Mengubah Background Utama Aplikasi (Gradasi Warna Soft) */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 2. Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic) */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 3. Mempercantik Tampilan Teks Judul */
    .main-title {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1e293b;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul dengan Gaya Baru
st.markdown('<div class="main-title">💬 Gemini Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten Pintar berbasis AI dengan Google Search Grounding</div>', unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) # Logo Variasi di Sidebar
    st.subheader("Panel Kontrol")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# 3. Validasi API Key
if not google_api_key:
    st.info("🔑 Silakan masukkan Google AI API Key Anda di menu sidebar untuk memulai percakapan.")
    st.stop()

# 4. Simpan Riwayat Pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tombol Reset Percakapan
if reset_button:
    st.session_state.messages = []
    st.rerun()

# 5. Tampilkan Welcome Message jika belum ada obrolan
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").markdown("Halo! Saya adalah asisten AI pro yang dilengkapi dengan pencarian Google secara *real-time*. Ada yang bisa saya bantu hari ini?")

# 6. Tampilkan Riwayat Obrolan di Layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 7. Proses Input Pesan Baru dari User
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    # Tampilkan dan simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Tampilkan respon dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        # FITUR MENARIK: Status Loading saat mencari data
        with st.spinner("🔍 Sedang menjelajahi Google & merumuskan jawaban terbaik..."):
            try:
                # Buat koneksi client baru
                client = genai.Client(api_key=google_api_key)

                # Gabungkan riwayat pesan
                full_prompt = "Kamu adalah asisten AI yang ramah dan profesional. Berikut adalah riwayat obrolan kita:\n"
                for msg in st.session_state.messages:
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += "assistant: "

                # Panggil model utama dengan Google Search
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}],
                        system_instruction="Jawablah menggunakan data paling valid dan terbaru dari Google Search."
                    )
                )

                # Tampilkan hasil respon di layar browser
                message_placeholder.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})

            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
