import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: CSS ANIMASI PC, CHAT & AVATAR HIDUP ====================
st.markdown("""
    <style>
    /* 1. Background Utama */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%);
    }
    
    /* 2. Sidebar Glassmorphic */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* 3. Animasi Judul Melayang & Bergeser Warna */
    @keyframes floatAndGlow {
        0% { transform: translateY(0px); background-position: 0% 50%; }
        50% { transform: translateY(-8px); background-position: 100% 50%; }
        100% { transform: translateY(0px); background-position: 0% 50%; }
    }
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 5px;
        background: linear-gradient(270deg, #2563eb, #9333ea, #3b82f6, #06b6d4);
        background-size: 400% 400%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: floatAndGlow 4s ease-in-out infinite;
    }
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 15px;
    }
    
    /* 4. FITUR BARU: Gambar PC Bergerak Aktif (Spin, Float, & Pulse) */
    @keyframes pcActiveAnimation {
        0% { transform: translateY(0px) rotate(0deg) scale(1); filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }
        25% { transform: translateY(-6px) rotate(2deg) scale(1.03); filter: drop-shadow(0 15px 20px rgba(37,99,235,0.2)); }
        50% { transform: translateY(0px) rotate(0deg) scale(1); filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }
        75% { transform: translateY(-6px) rotate(-2deg) scale(1.03); filter: drop-shadow(0 15px 20px rgba(147,51,234,0.2)); }
        100% { transform: translateY(0px) rotate(0deg) scale(1); filter: drop-shadow(0 4px 6px rgba(0,0,0,0.1)); }
    }
    .pc-container {
        display: flex;
        justify-content: center;
        margin-bottom: 25px;
    }
    .pc-image {
        width: 110px;
        animation: pcActiveAnimation 5s ease-in-out infinite;
    }
    
    /* 5. Animasi Bergerak Muncul pada Balon Chat */
    @keyframes chatPopUp {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
    [data-testid="stChatMessage"] {
        animation: chatPopUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* 6. Animasi Karakter Avatar Lebih Hidup */
    [data-testid="stChatMessage"] img[src*="user"] {
        content: url("https://cdn-icons-png.flaticon.com/512/4140/4140037.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stChatMessage"] img[src*="assistant"] {
        content: url("https://cdn-icons-png.flaticon.com/512/8943/8943377.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.3);
        transition: all 0.3s ease-in-out;
    }
    [data-testid="stChatMessage"]:hover img {
        transform: scale(1.2) rotate(8deg);
    }
    
    .time-text {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul & Elemen PC Bergerak Aktif
st.markdown('<div class="main-title">💻 Gemini SQL Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Database Agent • 20 Real Voices • Efek Visual Aktif Bergerak</div>', unsafe_allow_html=True)

# Memunculkan gambar PC Animasi Bergerak Aktif di halaman utama
st.markdown("""
    <div class="pc-container">
        <img class="pc-image" src="https://cdn-icons-png.flaticon.com/512/2004/2004699.png" alt="PC Gaming 3D">
    </div>
""", unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) 
    st.subheader("Panel Kontrol")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    
    st.markdown("---")
    st.subheader("🔊 Pengaturan Suara Realistis")
    enable_voice = st.checkbox("Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    # FITUR BARU: Dropdown 20 Karakter Suara Realistis (10 Pria & 10 Wanita)
    voice_character = st.selectbox(
        "Pilih Profil Suara Manusia Real:",
        [
            "👩 1. Sari (Customer Service - Ramah & Lembut)",
            "👩 2. Sinta (Penyiar Berita - Formal & Tegas)",
            "👩 3. Amanda (Gamer Girl - Ceria & Cepat)",
            "👩 4. Citra (Eksekutif Kantor - Tenang & Berwibawa)",
            "👩 5. Dian (Gadis Remaja - Santai & Gaul)",
            "👩 6. Ratu (Kasir Toko - Cepat & Sigap)",
            "👩 7. Maya (Dosen Tekno - Jelas & Edukatif)",
            "👩 8. Bella (Resepsionis - Manis & Sopan)",
            "👩 9. Indah (Podcaster - Hangat & Berenergi)",
            "👩 10. Fitri (Asisten Bisnis - Presisi & Profesional)",
            "👨 11. Budi (Manager Toko - Berat & Karismatik)",
            "👨 12. Rendi (Tech Reviewer - Cepat & Antusias)",
            "👨 13. Adi (Penyiar Radio - Renyah & Ramah)",
            "👨 14. Gunawan (Direktur Senior - Lambat & Tegas)",
            "👨 15. Kevin (Gamers Pro - Santai & Energetik)",
            "👨 16. Doni (Sales Promotor - Semangat & Nyaring)",
            "👨 17. Eko (Guru Komputer - Sabar & Tertata)",
            "👨 18. Fajar (Anak Senja - Tenang & Melow)",
            "👨 19. Hendra (Analis Data - Monoton & Serius)",
            "👨 20. Yusuf (Ustadz/Motivator - Teduh & Kalem)"
        ]
    )
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# Pemetaan konfigurasi parameter 20 suara (pitch & rate) untuk manipulasi Web Speech API
voice_params = {
    "👩 1. Sari (Customer Service - Ramah & Lembut)": {"pitch": 1.2, "rate": 0.95},
    "👩 2. Sinta (Penyiar Berita - Formal & Tegas)": {"pitch": 1.0, "rate": 1.1},
    "👩 3. Amanda (Gamer Girl - Ceria & Cepat)": {"pitch": 1.3, "rate": 1.2},
    "👩 4. Citra (Eksekutif Kantor - Tenang & Berwibawa)": {"pitch": 1.1, "rate": 0.9},
    "👩 5. Dian (Gadis Remaja - Santai & Gaul)": {"pitch": 1.25, "rate": 1.05},
    "👩 6. Ratu (Kasir Toko - Cepat & Sigap)": {"pitch": 1.15, "rate": 1.25},
    "👩 7. Maya (Dosen Tekno - Jelas & Edukatif)": {"pitch": 1.05, "rate": 0.95},
    "👩 8. Bella (Resepsionis - Manis & Sopan)": {"pitch": 1.2, "rate": 0.9},
    "👩 9. Indah (Podcaster - Hangat & Berenergi)": {"pitch": 1.15, "rate": 1.15},
    "👩 10. Fitri (Asisten Bisnis - Presisi & Profesional)": {"pitch": 1.1, "rate": 1.0},
    "👨 11. Budi (Manager Toko - Berat & Karismatik)": {"pitch": 0.65, "rate": 0.9},
    "👨 12. Rendi (Tech Reviewer - Cepat & Antusias)": {"pitch": 0.85, "rate": 1.2},
    "👨 13. Adi (Penyiar Radio - Renyah & Ramah)": {"pitch": 0.9, "rate": 1.05},
    "👨 14. Gunawan (Direktur Senior - Lambat & Tegas)": {"pitch": 0.7, "rate": 0.8},
    "👨 15. Kevin (Gamers Pro - Santai & Energetik)": {"pitch": 0.8, "rate": 1.15},
    "👨 16. Doni (Sales Promotor - Semangat & Nyaring)": {"pitch": 0.95, "rate": 1.3},
    "👨 17. Eko (Guru Komputer - Sabar & Tertata)": {"pitch": 0.85, "rate": 0.95},
    "👨 18. Fajar (Anak Senja - Tenang & Melow)": {"pitch": 0.75, "rate": 0.85},
    "👨 19. Hendra (Analis Data - Monoton & Serius)": {"pitch": 0.8, "rate": 0.95},
    "👨 20. Yusuf (Ustadz/Motivator - Teduh & Kalem)": {"pitch": 0.7, "rate": 0.85}
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

if reset_button:
    st.session_state.messages = []
    st.rerun()

# 6. Welcome Message
if len(st.session_state.messages) == 0:
    st.chat_message("assistant").markdown("Halo! Saya adalah AI profesional database toko komputer Anda. Desain grafis PC di atas bergerak aktif dan kini saya dilengkapi dengan **20 pilihan warna suara pria & wanita** yang sangat mirip dengan karakter asli di kehidupan nyata. Silakan berikan pertanyaan Anda!")

# 7. Tampilkan Riwayat Obrolan
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.markdown(f'<div class="time-text">{msg["time"]}</div>', unsafe_allow_html=True)

# 8. Input Chat Baru
if prompt := st.chat_input("Ketik pertanyaan seputar database di sini..."):
    current_time = datetime.now().strftime("%H:%M")
    
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.markdown(f'<div class="time-text">{current_time}</div>', unsafe_allow_html=True)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🔍 Menganalisis alur kerja SQL & merumuskan jawaban terbaik..."):
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

                # Typing Effect
                displayed_text = ""
                for char in response_text:
                    displayed_text += char
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.002)
                
                message_placeholder.markdown(response_text)
                
                bot_time = datetime.now().strftime("%H:%M")
                st.markdown(f'<div class="time-text">{bot_time}</div>', unsafe_allow_html=True)
                st.session_state.messages.append({"role": "assistant", "content": response_text, "time": bot_time})

                # FITUR MENGELUARKAN SUARA (20 KARAKTER REALISTIS)
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
                        if(voices[i].lang.indexOf('id') > -1) {{
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
