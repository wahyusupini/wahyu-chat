import streamlit as st
from google import genai
from google.genai import types
from datetime import datetime
import time

# 1. Konfigurasi Halaman Utama
st.set_page_config(page_title="Gemini SQL Chatbot Pro", page_icon="💻", layout="centered")

# ==================== FITUR MENARIK: CUSTOM CSS BACKGROUND & ANIMASI DINAMIS ====================
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
    
    /* 3. FITUR KEREN: Judul Bergerak Melayang & Berubah Warna */
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
        margin-bottom: 25px;
    }
    
    /* 4. FITUR BARU: Animasi Bergerak Muncul pada Balon Chat & Karater (Avatar) */
    @keyframes chatPopUp {
        0% {
            opacity: 0;
            transform: translateY(20px) scale(0.98);
        }
        100% {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Menerapkan efek bergerak halus pada setiap elemen chat di halaman */
    [data-testid="stChatMessage"] {
        animation: chatPopUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Efek sedikit interaktif saat kursor menyentuh balon chat */
    [data-testid="stChatMessage"]:hover {
        transform: translateY(-2px);
        transition: transform 0.2s ease;
    }
    
    /* 5. Gaya Teks Waktu (Timestamp) */
    .time-text {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: -10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul Dinamis
st.markdown('<div class="main-title">💻 Gemini SQL Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Database Agent • Animasi Obrolan Bergerak • Suara Pria/Wanita</div>', unsafe_allow_html=True)

# 2. Sidebar Pengaturan
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/6125/6125643.png", width=80) 
    st.subheader("Panel Kontrol")
    google_api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan API Key Anda...")
    
    st.markdown("---")
    st.subheader("🔊 Pengaturan Suara")
    enable_voice = st.checkbox("Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    # Pilihan Karakter Suara Pria dan Wanita
    voice_character = st.selectbox(
        "Pilih Karakter Suara:",
        [
            "Wanita (Sari - Lembut & Ramah)", 
            "Wanita (Sinta - Tegas & Formal)", 
            "Pria (Budi - Berat & Karismatik)", 
            "Pria (Rendi - Cepat & Energetik)"
        ]
    )
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# Pengaturan parameter pitch & rate suara
voice_params = {
    "Wanita (Sari - Lembut & Ramah)": {"pitch": 1.2, "rate": 0.95},
    "Wanita (Sinta - Tegas & Formal)": {"pitch": 1.1, "rate": 1.05},
    "Pria (Budi - Berat & Karismatik)": {"pitch": 0.7, "rate": 0.9},
    "Pria (Rendi - Cepat & Energetik)": {"pitch": 0.85, "rate": 1.15}
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
    st.info("🔑 Silakan masukkan Google AI API Key Anda di menu sidebar untuk memulai analisis database.")
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
    st.chat_message("assistant").markdown("Halo! Saya adalah AI profesional database toko komputer Anda. Sekarang seluruh balon obrolan dan karakter kita akan muncul dengan efek gerakan transisi yang halus! Silakan berikan pertanyaan Anda.")

# 7. Tampilkan Riwayat Obrolan beserta Timestamp di Layar (Otomatis Bergerak saat Dimuat)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        st.markdown(f'<div class="time-text">{msg["time"]}</div>', unsafe_allow_html=True)

# 8. Proses Input Pesan Baru dari User
if prompt := st.chat_input("Ketik pertanyaan terkait database atau produk di sini..."):
    current_time = datetime.now().strftime("%H:%M")
    
    # Tampilkan dan simpan pesan user (Efek bergerak dipicu secara otomatis oleh CSS)
    st.session_state.messages.append({"role": "user", "content": prompt, "time": current_time})
    with st.chat_message("user"):
        st.markdown(prompt)
        st.markdown(f'<div class="time-text">{current_time}</div>', unsafe_allow_html=True)

    # Tampilkan respon dari Gemini
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner("🔍 Memeriksa alur kerja SQL & merumuskan jawaban terbaik..."):
            try:
                # Buat koneksi client baru
                client = genai.Client(api_key=google_api_key)

                # Gabungkan riwayat pesan
                full_prompt = "Berikut adalah riwayat obrolan kita:\n"
                for msg in st.session_state.messages:
                    full_prompt += f"{msg['role']}: {msg['content']}\n"
                full_prompt += "assistant: "

                # Panggil model utama
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
                
                # Tampilkan teks final yang bersih
                message_placeholder.markdown(response_text)
                
                # Tampilkan Waktu Respons Bot
                bot_time = datetime.now().strftime("%H:%M")
                st.markdown(f'<div class="time-text">{bot_time}</div>', unsafe_allow_html=True)
                
                # Simpan ke riwayat
                st.session_state.messages.append({"role": "assistant", "content": response_text, "time": bot_time})

                # Mengeluarkan Suara Sesuai Pilihan (Pria/Wanita) via Web Speech API
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
