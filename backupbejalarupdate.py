import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini Chatbot Pro", page_icon="💬", layout="centered")

# ==================== FITUR MENARIK: CUSTOM CSS BACKGROUND & ANIMASI ====================
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
    
    /* 4. Gaya Teks Waktu (Timestamp) */
    .time-text {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul dengan Gaya Baru
st.markdown('<div class="main-title">💬 Gemini Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Asisten Pintar dengan Google Search Grounding & Fitur Suara</div>', unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) 
    st.subheader("Panel Kontrol")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    
    st.markdown("---")
    st.subheader("🤖 Personalisasi Bot")
    # FITUR MENARIK: Pilihan Karakter Bot
    bot_mood = st.selectbox(
        "Pilih Karakter Bot:",
        ["Profesional & Formal", "Ramah & Santai", "Humoris & Santai", "Pendidik/Guru"]
    )
    
    # FITUR MENARIK: Kontrol Suara
    enable_voice = st.checkbox("🔊 Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# Pemetaan instruksi sistem berdasarkan mood yang dipilih
mood_instructions = {
    "Profesional & Formal": "Jawablah dengan bahasa yang sangat profesional, formal, sopan, struktur yang rapi, dan berbasis data dari Google Search.",
    "Ramah & Santai": "Jawablah dengan gaya bahasa yang ramah, hangat, menggunakan panggilan akrab, mudah dimengerti, dan informatif.",
    "Humoris & Santai": "Jawablah dengan menyelipkan sedikit humor, santai, jenaka, namun tetap memberikan informasi akurat dari Google Search.",
    "Pendidik/Guru": "Jawablah dengan metode penjelasan yang edukatif, terstruktur langkah demi langkah seperti seorang guru mengajar muridnya."
}

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
    st.chat_message("assistant").markdown("Halo! Saya adalah asisten AI pro yang dilengkapi dengan pencarian Google secara *real-time* dan fitur suara. Ada yang bisa saya bantu hari ini?")

# 6. Tampilkan Riwayat Obrolan beserta Timestamp di Layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.markdown(f'<div class="time-text">{msg["time"]}</div>', unsafe_allow_html=True)

# 7. Proses Input Pesan Baru dari User
if prompt := st.chat_input("Ketik pesanmu di sini..."):
    current_time = datetime.now().strftime("%H:%M")
    
    # Tampilkan dan simpan pesan user
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.markdown(f'<div class="time-text">{current_time}</div>', unsafe_allow_html=True)

    # Tampilkan respon dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🔍 Sedang menjelajahi Google & merumuskan jawaban terbaik..."):
            try:
                # Buat koneksi client baru
                client = genai.Client(api_key=google_api_key)

                # Gabungkan riwayat pesan
                full_prompt = "Berikut adalah riwayat obrolan kita:\n"
                for msg in st.session_state.messages:
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += "assistant: "

                # Gabungkan instruksi dasar dengan mood pilihan pengguna
                system_instruction = f"Jawablah menggunakan data paling valid dan terbaru dari Google Search. {mood_instructions[bot_mood]}"

                # Panggil model utama dengan Google Search
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}],
                        system_instruction=system_instruction
                    )
                )

                response_text = response.text

                # FITUR MENARIK: Animasi Mengetik (Typing Effect)
                displayed_text = ""
                for char in response_text:
                    displayed_text += char
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.002) # Kecepatan teks muncul
                
                # Tampilkan teks final yang bersih
                message_placeholder.markdown(response_text)
                
                # Tampilkan Waktu
                bot_time = datetime.now().strftime("%H:%M")
                st.markdown(f'<div class="time-text">{bot_time}</div>', unsafe_allow_html=True)
                
                # Simpan ke riwayat
                st.session_state.messages.append({"role": "assistant", "content": response_text, "time": bot_time})

                # FITUR MENARIK: Mengeluarkan Suara (Web Speech API)
                if enable_voice:
                    # Menghapus simbol markdown agar suara membaca dengan bersih
                    clean_text = response_text.replace("*", "").replace("#", "").replace("`", "")
                    
                    # Menggunakan komponen HTML/JS untuk menyuruh browser berbicara
                    components_code = f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance({repr(clean_text)});
                    msg.lang = 'id-ID'; // Mengatur suara dalam bahasa Indonesia
                    window.speechSynthesis.speak(msg);
                    </script>
                    """
                    st.components.v1.html(components_code, height=0, width=0)

            except Exception as e:
                st.error(f"Terjadi kendala: {e}")
