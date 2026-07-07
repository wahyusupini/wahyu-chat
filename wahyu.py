import streamlit as st
from google import genai
from google.genai import types

# =====================================================================
# 1. KONFIGURASI API KEY (Sudah dibungkus tanda kutip dengan benar)
# =====================================================================
GEMINI_API_KEY = "AQ.Ab8RN6KYRa7OvT1O6RayeQCeD2RcL8_B0EABc5yrK7WS9ZH75w"

# Inisialisasi Google GenAI Client menggunakan variabel API Key
client = genai.Client(api_key=GEMINI_API_KEY)

# =====================================================================
# 2. KONFIGURASI HALAMAN STREAMLIT
# =====================================================================
st.set_page_config(
    page_title="HyperTune AI - Parameter Convergence Chatbot",
    page_icon="🤖",
    layout="centered"
)
st.title("🤖 HyperTune AI")
st.subheader("Asisten Konvergensi Parameter & Optimasi Model")
st.write("Diskusikan metrik, loss curves, dan tuning hyperparameter model Anda di sini.")

# System Instruction versi linear (Aman dari semua jenis Error Indentasi/Syntax Windows)
system_instruction = (
    "Anda adalah HyperTune AI, seorang Profesor dan Penasihat Akademik Senior di bidang Machine Learning dan Optimasi Numerik.\n\n"
    "Karakter & Sifat Anda:\n"
    "1. Intelektual Tingkat Tinggi: Anda berbicara dengan artikulasi yang jernih, tenang, berwibawa, dan menggunakan bahasa Indonesia ilmiah yang baku namun mengalir alami.\n"
    "2. Rasional & Metodologis: Anda menghargai batasan epistemologis (ruang lingkup keilmuan) dan selalu mengarahkan diskusi ke arah pembuktian empiris.\n"
    "3. Mentor yang Bijak: Anda tidak hanya memberikan jawaban instan, tetapi memicu pengguna untuk berpikir secara struktural mengenai arsitektur dan parameter model mereka.\n\n"
    "ATURAN KETAT (Jika mendeteksi pertanyaan di luar Data Science seperti politik, presiden, atau dinamika sosial):\n"
    "Jawablah dengan perspektif seorang Profesor yang menghargai batasan keahlian, menggunakan kalimat berikut:\n\n"
    "Sebagai seorang akademisi yang mendedikasikan fokus riset pada domain Machine Learning dan optimasi parameter, saya memiliki tanggung jawab ilmiah untuk hanya memberikan keputusan atau analisis pada wilayah kepakaran saya. Dinamika sosial-politik, struktur pemerintahan, maupun figur publik merupakan ranah kajian yang berada di luar domain kompetensi dan batas riset saya. Oleh karena itu, saya tidak memiliki kapasitas akademik yang valid untuk memberikan pandangan atas topik tersebut.\n\n"
    "Mari kita kembalikan fokus diskusi pada substansi yang lebih produktif bagi riset Anda. Jika Anda sedang menghadapi kendala terkait perilaku konvergensi parameter, seperti stagnasi pada kurva loss, instabilitas gradien, atau sedang mengevaluasi trade-off antara algoritma Adam dan SGD pada lanskap optimasi Anda, silakan paparkan data eksperimen atau metrik yang Anda miliki. Kita akan bedah pemodelannya secara metodologis."
)

# =====================================================================
# 3. MANAJEMEN RIWAYAT CHAT (SESSION STATE)
# =====================================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

# Menampilkan riwayat chat yang sudah ada di layar
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================================
# 4. PROSES INPUT USER DAN RESPON GEMINI
# =====================================================================
if user_input := st.chat_input("Tanyakan sesuatu tentang konvergensi parameter..."):

    # 1. Tampilkan chat dari user di UI
    with st.chat_message("user"):
        st.markdown(user_input)

    # Simpan chat user ke dalam session history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # 2. Panggil Gemini API untuk mendapatkan respon
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("*Sedang berpikir...*")

        # Inisialisasi variabel respons untuk mekanisme fallback jika server sibuk
        response = None

        # Percobaan 1: Menggunakan model andalan terbaru gemini-2.5-flash
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_input,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7,
                ),
            )
        except Exception as e_flash:
            # Jika terjadi error 503 (High Demand) pada model terbaru, otomatis beralih ke cadangan
            if "503" in str(e_flash) or "UNAVAILABLE" in str(e_flash):
                try:
                    # Percobaan 2: Menggunakan model alternatif gemini-2.0-flash yang lebih stabil
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=user_input,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.7,
                        ),
                    )
                except Exception as e_backup:
                    error_msg = f"Terjadi kesalahan pada server cadangan: {str(e_backup)}"
                    message_placeholder.error(error_msg)
            else:
                # Menangkap error lain di luar server sibuk (misal key salah atau permission denied)
                error_msg = f"Terjadi kesalahan pada API: {str(e_flash)}"
                message_placeholder.error(error_msg)

        # Jika berhasil mendapatkan respons dari salah satu model, tampilkan ke UI
        if response is not None:
            ai_response = response.text
            message_placeholder.markdown(ai_response)

            # Simpan respon AI ke dalam session history
            st.session_state.messages.append({"role": "assistant", "content": ai_response})