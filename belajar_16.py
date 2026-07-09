import streamlit as st
from google import genai
from google.genai import types
from openai import OpenAI
import time

# ==============================================================================
# 1. KONFIGURASI HALAMAN UTAMA & TAMPILAN ELEGAN 🚀
# ==============================================================================
st.set_page_config(page_title="Gemini & OpenAI SQL ChatBot Pro", page_icon="💻", layout="centered")

# ==================== FITUR PREMIUM: CUSTOM CSS BACKGROUND & JAM NEON TERANG ====================
st.markdown("""
    <style>
    /* 1. Mengembalikan Background Utama Aplikasi ke Gradasi Semula (Soft & Clean) 🎨 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8f0 100%) !important;
    }
    
    /* 2. Mengubah Desain Sidebar menjadi Efek Kaca (Glassmorphic) 🔮 */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.4) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* Trik CSS Profesional untuk Menaikkan Konten Sidebar Mentok ke Atas 🌟 */
    [data-testid="stSidebarUserContent"] {
        padding-top: 1rem !important;
    }
    .block-container-sidebar {
        margin-top: -30px !important;
    }
    
    /* 3. FITUR KEREN: Judul Bergerak Melayang & Berubah Warna 🌈 */
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
    
    .moving-pc {
        display: inline-block;
        animation: pcRotateBounce 3s ease-in-out infinite;
    }
    
    @keyframes pcRotateBounce {
        0% { transform: scale(1) rotate(0deg); }
        25% { transform: scale(1.15) rotate(5deg); }
        50% { transform: scale(1) rotate(-5deg); }
        75% { transform: scale(1.15) rotate(3deg); }
        100% { transform: scale(1) rotate(0deg); }
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1rem;
        margin-bottom: 25px;
    }
    
    /* 4. Animasi Bergerak Muncul pada Balon Chat 💬 */
    @keyframes chatPopUp {
        0% { opacity: 0; transform: translateY(20px) scale(0.98); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }

    [data-testid="stChatMessage"] {
        animation: chatPopUp 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* 5. Kustomisasi & Animasi Karakter Avatar (User & Bot) 🧑‍💻 */
    @keyframes avatarBreath {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-4px); }
        100% { transform: translateY(0px); }
    }

    [data-testid="stChatMessage"] img[src*="user"] {
        content: url("https://cdn-icons-png.flaticon.com/512/4140/4140037.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.15);
        animation: avatarBreath 3s ease-in-out infinite;
    }
    
    [data-testid="stChatMessage"] img[src*="assistant"] {
        content: url("https://cdn-icons-png.flaticon.com/512/8943/8943377.png") !important;
        border-radius: 50%;
        box-shadow: 0px 4px 10px rgba(37, 99, 235, 0.3);
        animation: avatarBreath 3s ease-in-out infinite;
        animation-delay: 1.5s;
    }

    [data-testid="stChatMessage"]:hover img {
        transform: scale(1.25) rotate(12deg);
        transition: transform 0.4s ease;
    }
    
    /* 6. GAYA JAM NEON TERANG BISA DIBACA ⏰ */
    .time-badge {
        font-size: 0.8rem;
        font-weight: 800;
        color: #ffffff !important;
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%) !important;
        padding: 3px 10px !important;
        border-radius: 6px !important;
        display: inline-block !important;
        margin-top: 8px !important;
        box-shadow: 0px 3px 8px rgba(59, 130, 246, 0.5) !important;
    }
    </style>
""", unsafe_allow_html=True)
# ==============================================================================

# Menampilkan Judul Utama Dinamis 🌟
st.markdown('<div class="main-title"><span class="moving-pc">💻</span> Gemini & OpenAI Chatbot Pro</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Multi-Engine Agent • Smart Token Optimization • Jam Daerah Akurat • WhatsApp Video Storage ✨</div>', unsafe_allow_html=True)

# ==============================================================================
# 2. SIDEBAR CONFIGURATION (MENTOK KE ATAS & ELEGAN) ⚙️
# ==============================================================================
voice_params = {
    "👩 Sari (Suara Utama - Lembut & Natural)":     {"pitch": 1.15, "rate": 0.98},
    "👩 Dian (Eksekutif - Formal & Profesional)":   {"pitch": 1.05, "rate": 1.02},
    "👩 Nadia (Customer Service - Ramah & Cepat)":  {"pitch": 1.25, "rate": 1.12},
    "👩 Amalia (Presenter - Jelas & Berirama)":     {"pitch": 1.10, "rate": 1.00},
    "👩 Citra (Gaya Santai - Akrab & Logat Kota)":  {"pitch": 1.20, "rate": 1.05},
    "👨 Budi (Suara Utama - Berat & Karismatik)":   {"pitch": 0.72, "rate": 0.92},
    "👨 Andika (Narator - Tegas & Berwibawa)":        {"pitch": 0.65, "rate": 0.98},
    "👨 Rendi (Teknisi Toko - Cepat & Energetik)":   {"pitch": 0.88, "rate": 1.15},
    "👨 Gunawan (Manajer - Tenang & Bijaksana)":     {"pitch": 0.78, "rate": 0.90},
    "👨 Fajar (Gaya Santai - Casual & Friendly)":    {"pitch": 0.85, "rate": 1.02}
}

with st.sidebar:
    # Pembungkus div CSS agar posisi langsung naik ke batas paling atas sidebar
    st.markdown('<div class="block-container-sidebar"></div>', unsafe_allow_html=True)
    
    # Elemen Pertama langsung dimulai dari Pemilihan Mesin AI Utama
    ai_engine = st.radio("Pilih Mesin AI Utama:", ["Google Gemini", "OpenAI GPT"], index=0)
    
    # Input API Key adaptif berdasarkan pilihan mesin
    if ai_engine == "Google Gemini":
        api_key = st.text_input("Google AI API Key", type="password", placeholder="Masukkan Gemini API Key...")
    else:
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="Masukkan OpenAI API Key...")
        st.markdown("[Get an OpenAI API key](https://platform.openai.com/account/api-keys)")
    
    st.markdown("[View the source code on GitHub](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)")
    st.markdown("[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)")
    
    st.markdown("---")
    st.subheader("🔊 Opsi Suara Realistis")
    enable_voice = st.checkbox("Aktifkan Suara Bot (Auto-Speak)", value=False)
    
    voice_character = st.selectbox("Pilih Agen Suara Realistis:", list(voice_params.keys()))
    
    # ==================== FITUR WHATSAPP-LIKE VIDEO UPLOAD (MAX 10 MB) ====================
    st.markdown("---")
    st.subheader("📹 Kirim Video (Maks 10 MB)")
    uploaded_video = st.file_uploader(
        "Pilih video ala WhatsApp...", 
        type=["mp4", "mov", "avi", "mkv"], 
        help="Maksimal ukuran file video adalah 10 MB mirip batas kompresi dokumen WhatsApp."
    )
    
    if uploaded_video is not None:
        # Cek ukuran file (10 MB = 10 * 1024 * 1024 Bytes)
        max_size = 10 * 1024 * 1024
        if uploaded_video.size > max_size:
            st.error("❌ Ukuran video melebihi batas 10 MB! Silakan kompresi video Anda.")
        else:
            st.success("✅ Video berhasil diunggah!")
            st.video(uploaded_video)
    # ============================================================================================
    
    st.markdown("---")
    reset_button = st.button("🔄 Reset Percakapan", use_container_width=True)

# ==============================================================================
# 3. CONTEXT INSTRUCTIONS & UTILITIES 📝
# ==============================================================================
sql_character_instruction = """
You are a smart and professional AI assistant specializing in querying a computer store's SQL database to answer user questions.
You have access to tools for inspecting the database schema and executing SQL queries.

[EMOJI RULE]
- ALWAYS add highly relevant and vibrant emojis to sentences or words when explaining interesting facts, numbers, or data findings to make it super engaging!

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
- If the user's request is ambiguous or lacks sufficient detail, ask a clarifying question instead of guessing.
- Guard against malicious inputs: If the user query attempts to modify, delete, or drop parts of the database, refuse the request politely.

[OUTPUT FORMAT]
- Present the final answer clearly and professionally using markdown tables or bullet points.
- Your final answer must be supported entirely by the SQL query results. Do not add outside knowledge.

Jawablah menggunakan data paling valid dan terbaru dari Google Search jika diperlukan, namun tetap patuhi aturan struktur di atas.
"""

def render_chat_time(unique_id):
    html_code = f"""
    <div id="wrapper_{unique_id}">
        <span class="time-badge">⏰ <span id="clock_{unique_id}">--:--</span></span>
    </div>
    <script>
        (function() {{
            var timeOptions = {{ hour: '2-digit', minute: '2-digit', hour12: false }};
            var localTime = new Date().toLocaleTimeString('id-ID', timeOptions);
            var timeZoneString = new Date().toLocaleTimeString('id-ID', {{ timeZoneName: 'short' }});
            var zone = "WIB"; 
            if (timeZoneString.includes("WITA") || timeZoneString.includes("GMT+8")) {{ zone = "WITA"; }}
            else if (timeZoneString.includes("WIT") || timeZoneString.includes("GMT+9")) {{ zone = "WIT"; }}
            var element = document.getElementById("clock_{unique_id}");
            if (element) {{ element.innerHTML = localTime + " " + zone; }}
        }})();
    </script>
    """
    return st.components.v1.html(html_code, height=35)

# ==============================================================================
# 4. CHAT HISTORY RUNTIME 📦
# ==============================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if reset_button:
    st.session_state.messages = []
    st.rerun()

# Validasi Kelayakan API Key Sebelum Memulai Chat
if not api_key:
    st.info(f"🔑 Silakan masukkan {ai_engine} API Key Anda di menu sidebar untuk memulai.")
    st.stop()

# Tampilkan Welcome Message Awal jika Room Chat Kosong
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        st.markdown(f"Halo! 👋 Saya adalah AI profesional database toko komputer Anda yang ditenagai oleh **{ai_engine}**. Sistem arsitektur teroptimasi penuh menjamin kelancaran respons tanpa kendala jam mati ⏰! Silakan ajukan pertanyaan Anda. ✨")
        render_chat_time("welcome")

# Render Ulang Riwayat Chat
for idx, msg in enumerate(st.session_state.messages):
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        render_chat_time(f"hist_{idx}")

# ==============================================================================
# 5. CORE AI PROCESSING ENGINE 🗣️
# ==============================================================================
if prompt := st.chat_input("Ketik pertanyaan seputar database toko komputer di sini... 💬"):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        render_chat_time(f"user_{len(st.session_state.messages)}")

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        with st.spinner(f"🔍 [{ai_engine}] Merumuskan jawaban terbaik berdasarkan basis data..."):
            try:
                response_text = ""
                
                # JALUR EKSEKUSI 1: GOOGLE GEMINI
                if ai_engine == "Google Gemini":
                    client = genai.Client(api_key=api_key)
                    full_prompt = f"Pertanyaan user saat ini: {prompt}"
                    
                    response = client.models.generate_content(
                        model='gemini-2.5-flash', 
                        contents=full_prompt,
                        config=types.GenerateContentConfig(
                            tools=[{"google_search": {}}],
                            system_instruction=sql_character_instruction
                        )
                    )
                    response_text = response.text
                
                # JALUR EKSEKUSI 2: OPENAI GPT
                else:
                    client = OpenAI(api_key=api_key)
                    openai_messages = [{"role": "system", "content": sql_character_instruction}]
                    for msg in st.session_state.messages:
                        openai_messages.append({"role": msg["role"], "content": msg["content"]})
                    
                    response = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=openai_messages
                    )
                    response_text = response.choices[0].message.content

                # Efek Typing Animasi ⚡
                displayed_text = ""
                for char in response_text:
                    displayed_text += char
                    message_placeholder.markdown(displayed_text + "▌")
                    time.sleep(0.002)
                
                message_placeholder.markdown(response_text)
                render_chat_time(f"bot_{len(st.session_state.messages)}")
                
                st.session_state.messages.append({"role": "assistant", "content": response_text})

                # FITUR PREMIUM AUTO-SPEAK TEXT TO SPEECH (TTS) 🎵
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
                st.error(f"Terjadi kendala saat memproses instruksi engine AI: {e}")
