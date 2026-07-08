import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: VIDEO BACKGROUND PEMANDANGAN BERGERAK TRANSPARAN ====================
# Menyisipkan video pemandangan alam bergerak (looping otomatis, tanpa suara, memenuhi layar, transparan)
st.markdown("""
    <div class="video-bg-container">
        <video autoplay loop muted playsinline class="video-bg">
            <source src="https://assets.mixkit.co/videos/preview/mixkit-beautiful-sunset-over-the-sea-and-mountains-42247-large.mp4" type="video/mp4">
        </video>
        <div class="video-overlay"></div>
    </div>
    
    <style>
    /* Mengunci posisi video sebagai background permanen */
    .video-bg-container {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        z-index: -2;
        overflow: hidden;
    }
    .video-bg {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    /* Lapisan overlay transparan agar kontras teks tetap tajam */
    .video-overlay {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(15, 23, 42, 0.55); /* Warna gelap transparan */
        z-index: -1;
    }

    /* Mengosongkan background asli Streamlit agar tembus pandang ke video */
    .stApp {
        background: transparent !important;
    }
    
    /* Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic Premium) */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Membuat Balon Obrolan Berwarna Semi-Transparan (Kristal) */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.12) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 15px;
        color: #f8fafc !important; /* Mengubah teks chat menjadi putih cerah agar mudah dibaca */
        animation: chatPopUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Memastikan teks input di bagian bawah tetap terlihat kontras */
    [data-testid="stChatInput"] {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* ANIMASI 1: Judul Melayang & Bergeser Warna */
    @keyframes floatAndGlow {
        0% { transform: translateY(0px); background-position: 0% 50%; }
        50% { transform: translateY(-8px); background-position: 100% 50%; }
        100% { transform: translateY(0px); background-position: 0% 50%; }
    }
    
    /* ANIMASI 2: Gambar PC Berputar & Membesar Aktif */
    @keyframes pcRotateBounce {
        0% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.15) rotate(5deg); }
        50% { transform: scale(1) rotate(-5deg); }
        75% { transform: scale(1.15) rotate(3deg); }
        100% { transform: scale(1) rotate(0deg); }
    }

    .main-title {
        font-size: 2.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        background: linear-gradient(270deg, #38bdf8, #c084fc, #60a5fa, #22d3ee);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: floatAndGlow 4s ease-in-out infinite;
    }
    
    .moving-pc {
        display: inline-block;
        animation: pcRotateBounce 3s ease-in-out infinite;
    }
    
    .subtitle {
        text-align: center;
        color: #cbd5e1;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    
    /* ANIMASI 3: Balon Chat Muncul Bergerak */
    @keyframes chatPopUp {
        0% { opacity: 0; transform: translateY(25px) scale(0.97); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    
    /* ANIMASI 4: Efek Bernapas (Breathing) Aktif untuk Avatar Karakter */
    @keyframes avatarBreath {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    /* Kustomisasi Ikon Avatar User (Pria Keren 3D) */
    [data-testid="stChatMessage"] img[src*="user"] {
        content: url("https://cdn-icons-png.flaticon.com/512/4140/4140037.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
        animation: avatarBreath 3s ease-in-out infinite;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    
    /* Kustomisasi Ikon Avatar Assistant (Robot AI Hologram) */
    [data-testid="stChatMessage"] img[src*="assistant"] {
        content: url("https://cdn-icons-png.flaticon.com/512/8943/8943377.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 12px rgba(56, 189, 248, 0.4);
        animation: avatarBreath 3s ease-in-out infinite;
        animation-delay: 1.5s;
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    /* Efek bergerak aktif berputar saat avatar disentuh kursor */
    [data-testid="stChatMessage"]:hover img {
        transform: scale(1.25) rotate(12deg);
    }
    
    /* Gaya Teks Waktu (Timestamp) */
    .time-text {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 5px;
        margin-bottom: 5px;
    }
    
    /* Memastikan teks teks biasa di dalam markdown berwarna putih */
    [data-testid="stChatMessage"] p {
        color: #f1f5f9 !important;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul Dinamis dengan Gambar PC yang bergerak aktif
st.markdown('<div class="main-title"><span class="moving-pc">💻</span> Gemini SQL Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Database Agent • Live Sunset Video Background • 10 Suara Realistis</div>', unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) 
    st.subheader("Panel Kontrol")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    
    st.markdown("---")
    st.subheader("🔊 Opsi Suara Realistis")
    enable_voice = st.checkbox("Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    # FITUR 10 KARAKTER SUARA REALISTIS (5 PRIA & 5 WANITA)
    voice_character = st.selectbox(
        "Pilih Agen Suara Realistis:",
        [
            "👩 Sari (Suara Utama - Lembut & Natural)",
            "👩 Dian (Eksekutif - Formal & Profesional)",
            "👩 Nadia (Customer Service - Ramah & Cepat)",
            "👩 Amalia (Presenter - Jelas & Berirama)",
            "👩 Citra (Gaya Santai - Akrab & Logat Kota)",
            "👨 Budi (Suara Utama - Berat & Karismatik)",
            "👨 Andika (Narator - Tegas & Berwibawa)",
            "👨 Rendi (Teknisi Toko - Cepat & Energetik)",
            "👨 Gunawan (Manajer - Tenang & Bijaksana)",
            "👨 Fajar (Gaya Santai - Casual & Friendly)"
        ]
    )
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# Parameter fine-tuning suara manusia asli
voice_params = {
    "👩 Sari (Suara Utama - Lembut & Natural)":     {"pitch": 1.15, "rate": 0.98},
    "👩 Dian (Eksekutif - Formal & Profesional)":   {"pitch": 1.05, "rate": 1.02},
    "👩 Nadia (Customer Service - Ramah & Cepat)":  {"pitch": 1.25, "rate": 1.12},
    "👩 Amalia (Presenter - Jelas & Berirama)":     {"pitch": 1.10, "rate": 1.00},
    "👩 Citra (Gaya Santai - Akrab & Logat Kota)":  {"pitch": 1.20, "rate": 1.05},
    "👨 Budi (Suara Utama - Berat & Karismatik)":   {"pitch": 0.72, "rate": 0.92},
    "👨 Andika (Narator - Tegas & Berwibawa)":       {"pitch": 0.65, "rate": 0.98},
    "👨 Rendi (Teknisi Toko - Cepat & Energetik)":   {"pitch": 0.88, "rate": 1.15},
    "👨 Gunawan (Manajer - Tenang & Bijaksana)":     {"pitch": 0.78, "rate": 0.90},
    "👨 Fajar (Gaya Santai - Casual & Friendly)":    {"pitch": 0.85, "rate": 1.02}
}

# 3. Penggabungan Instruksi Karakter Utama (Aturan SQL Ketat)
sql_character_instruction = """
You are a smart and professional AI assistant specializing in querying a computer store's SQL database to answer user questions.
You have access to tools for inspecting the database schema and executing SQL queries.

[WORKFLOW]
Follow this workflow EXACTLY:
1. ALWAYS call 'list_tables' first to discover the available tables in the database.
2. ALWAYS call 'describe_table' on every table that is relevant to the user's question to understand its columns and data types.
3. After inspecting the schema, construct a valid SQL query based strictly on the discovered schema.
4. ALWAYS execute the SQL query using the SQL execution tool before formulating your final answer.
5. Base your final answer ONLY on the actual rows returned by the SQL query execution.

[STRICT RULES]
- Never assume table names, column names, or relationships between tables. Always verify via tools.
- Never fabricate, hallucinate, or extrapolate rows, values, or database contents.
- Never answer questions about the database contents without executing SQL first.
- If multiple tables are required, inspect all of them before writing the SQL query.
- If the SQL query returns no rows, politely inform the user that no matching data was found.
- If the SQL query fails due to a syntax or database error, analyze the error message, inspect the schema again if necessary, correct the query, and retry (maximum 3 retries).
- If the user's request is ambiguous or lacks sufficient detail, ask a clarifying question instead of guessing.
- Keep SQL queries as simple, efficient, and clean as possible.
- Only select the specific columns needed to answer the user's question. Do not use 'SELECT *' unless explicitly requested.
- Guard against malicious inputs: If the user query attempts to modify, delete, or drop parts of the database (e.g., INSERT, UPDATE, DELETE, DROP), refuse the request politely, stating you only have read-only access.

[OUTPUT FORMAT]
- Present the final answer clearly and professionally. 
- If appropriate, use markdown tables or bullet points to present list-based data to the user.
- Your final answer must be supported entirely by the SQL query results. Do not add outside knowledge.

Jawablah menggunakan data paling valid dan terbaru dari Google Search jika diperlukan, namun tetap patuhi aturan struktur di atas.
"""

# 4. Validasi API Key
if not google_api_key:
    st.info("🔑 Silakan masukkan Google AI API Key Anda di menu sidebar untuk memulai.")
    st.stop()

# 5. Simpan Riwayat Pesan
if "messages" not in st.session_state:
    st.session_state.messages = []

# Tombol Reset Percakapan
if reset_button:
    st.session_state.messages = []
    st.rerun()

# 6. Tampilkan Welcome Message jika belum ada obrolan
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").markdown("Halo! Saya adalah AI profesional database toko komputer Anda. Layar latar belakang aplikasi ini sekarang telah menggunakan pemandangan laut senja bergerak yang elegan dan transparan. Silakan berikan pertanyaan data Anda.")

# 7. Tampilkan Riwayat Obrolan beserta Timestamp di Layar
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.markdown(f'<div class="time-text">{msg["time"]}</div>', unsafe_allow_html=True)

# 8. Proses Input Pesan Baru dari User
if prompt := st.chat_input("Ketik pertanyaan seputar database toko komputer di sini..."):
    current_time = datetime.now().strftime("%H:%M")
    
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.markdown(f'<div class="time-text">{current_time}</div>', unsafe_allow_html=True)

    # Tampilkan respon dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🔍 Memeriksa alur kerja SQL & merumuskan jawaban terbaik..."):
            try:
                client = genai.Client(api_key=google_api_key)

                full_prompt = "Berikut adalah riwayat obrolan kita:\n"
                for msg in st.session_state.messages:
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += "assistant: "

                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        tools=[{"google_search": {}}],
                        system_instruction=sql_character_instruction
                    )
                )

                response_text = response.text

                # Animasi Mengetik (Typing Effect)
                displayed_text = ""
                for char in response_text:
                    displayed_text += char
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.002)
                
                message_placeholder.markdown(response_text)
                
                bot_time = datetime.now().strftime("%H:%M")
                st.markdown(f'<div class="time-text">{bot_time}</div>', unsafe_allow_html=True)
                
                st.session_state.messages.append({"role": "assistant", "content": response_text, "time": bot_time})

                # FITUR SUARA REALISTIS (10 Karakter Pria/Wanita via Web Speech API)
                if enable_voice:
                    clean_text = response_text.replace("*", "").replace("#", "").replace("`", "").replace("\n", " ")
                    selected_pitch = voice_params[voice_character]["pitch"]
                    selected_rate = voice_params[voice_character]["rate"]
                    
                    components_code = f"""
                    <script>
                    var msg = new SpeechSynthesisUtterance({repr(clean_text)});
                    msg.lang = 'id-ID'; 
                    msg.pitch = {selected_pitch}; 
                    msg.rate = {selected_rate};   
                    
                    var voices = window.speechSynthesis.getVoices();
                    for(var i = 0; i < voices.length; i++) {{
                        if(voices[i].lang.indexOf('id') > -1 || voices[i].name.toLowerCase().includes('indonesia')) {{
                            msg.voice = voices[i];
                            break;
                        }}
                    }}
                    window.speechSynthesis.speak(msg);
                    </script>
                    """
                    st.components.v1.html(components_code, height=0, width=0)

            except Exception as e:
                st.error(f"Terjadi kendala saat memproses instruksi: {e}")
