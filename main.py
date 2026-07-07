import moviepy
import cv2  # opencv-python diimpor dengan nama cv2
import PIL  # Pillow diimpor dengan nama PIL
import gtts
import pydub
import requests
import os
import re
import json
import requests
from duckduckgo_search import DDGS
import google.generativeai as genai
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import urllib.parse
import google.generativeai as genai


# ==========================================
# CONFIGURATION & API KEYS
# ==========================================
GEMINI_API_KEY = "AIzaSyCal0KCF0uoKXK0mEHZa4DYYdraBs8kyEY"  # Ganti dengan API Key Gemini Anda
genai.configure(api_key=GEMINI_API_KEY)
import google.generativeai as genai

genai.configure(api_key="AIzaSyCal0KCF0uoKXK0mEHZa4DYYdraBs8kyEY")

for m in genai.list_models():
    if "generateContent" in m.supported_generation_methods:
        print(m.name)

# Folder output untuk menyimpan aset sementara dan video final
OUTPUT_DIR = "output_assets"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==========================================
# STEP 1: SEARCH THE INTERNET (DuckDuckGo)
# ==========================================
def search_latest_trend(topic):
    print(f"[1/5] Mencari informasi terbaru tentang: {topic}...")
    with DDGS() as ddgs:
        results = [r for r in ddgs.text(topic, max_results=3)]

    combined_text = ""
    for res in results:
        combined_text += f"Title: {res['title']}\nSnippet: {res['body']}\n\n"
    return combined_text


# ==========================================
# STEP 2: GENERATE SCRIPT & PROMPTS (Gemini)
# ==========================================
def generate_script_with_gemini(internet_data, topic):
    print("[2/5] Meminta Gemini AI untuk membuat skrip dan prompt gambar...")
    model = genai.GenerativeModel('gemini-2.5-flash')

    prompt = f"""
    Kamu adalah seorang kreator konten YouTube sukses. Berdasarkan data internet berikut mengenai "{topic}":

    {internet_data}

    Buatlah sebuah skrip video YouTube pendek (sekitar 3 adegan). 
    Format output HARUS dalam bentuk JSON yang valid agar bisa diproses oleh kode Python. 
    Jangan berikan teks tambahan di luar JSON.

    Struktur JSON harus seperti ini:
    {{
      "scenes": [
        {{
          "scene_number": 1,
          "narration": "Teks yang akan diucapkan oleh voice over dalam bahasa Indonesia",
          "image_keyword": "1 atau 2 kata kunci bahasa inggris yang sangat spesifik untuk dicari di Unsplash untuk latar belakang visual"
        }},
        ...
      ]
    }}
    """

    response = model.generate_content(prompt)
    response_text = response.text

    # Membersihkan markdown jika Gemini membungkusnya dalam ```json
    if "```json" in response_text:
        response_text = re.search(r"```json(.*?)```", response_text, re.DOTALL).group(1)
    elif "```" in response_text:
        response_text = re.search(r"```(.*?)```", response_text, re.DOTALL).group(1)

    return json.loads(response_text.strip())


# ==========================================
# STEP 3: DOWNLOAD VISUAL ASSETS (Unsplash)
# ==========================================
def download_image(keyword, index):
    image_path = os.path.join(OUTPUT_DIR, f"image_{index}.jpg")
    print(f" Mengunduh gambar untuk adegan {index} dengan kata kunci: {keyword}...")
    # Menggunakan Source Unsplash gratis tanpa API key untuk kemudahan
    keyword_encoded = urllib.parse.quote(keyword)
    url = f"https://source.unsplash.com/featured/1920x1080/?{keyword_encoded}"
    response = requests.get(url)
    headers = {
        "Authorization": "d1DJXtOzVZKDPow58XaIqxObwtlkoZ2Bn7oYeJxfIbdl6W1TCqbZRXU1"
    }
    url = f"https://api.pexels.com/v1/search?query={keyword_encoded}&per_page=1"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            img_url = data["photos"][0]["src"]["large"]
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                with open(image_path, 'wb') as f:
                    f.write(img_response.content)
                return image_path




    image_path = os.path.join(OUTPUT_DIR, f"image_{index}.jpg")
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        return image_path
    else:
        print("Gagal mengunduh gambar, menggunakan gambar placeholder.")
        return None


# ==========================================
# STEP 4: GENERATE VOICE OVER (gTTS)
# ==========================================
def generate_voice_over(text, index):
    print(f" Membuat Voice Over untuk adegan {index}...")
    tts = gTTS(text=text, lang='id')
    audio_path = os.path.join(OUTPUT_DIR, f"audio_{index}.mp3")
    tts.save(audio_path)
    return audio_path


# ==========================================
# STEP 5: ASSEMBLE VIDEO (MoviePy)
# ==========================================
def create_final_video(script_data):
    print("[5/5] Merakit video menggunakan MoviePy...")
    video_clips = []

    for idx, scene in enumerate(script_data['scenes'], start=1):
        narration = scene['narration']
        keyword = scene['image_keyword']

        # Jalankan proses download & TTS
        img_path = download_image(keyword, idx)
        aud_path = generate_voice_over(narration, idx)

        if img_path and aud_path:
            # Memuat file audio untuk tahu durasinya
            audio_clip = AudioFileClip(aud_path)
            duration = audio_clip.duration

            # Membuat klip gambar dengan durasi sepanjang audio
            image_clip = ImageClip(img_path).set_duration(duration)
            # Pasangkan audio ke gambar
            video_clip = image_clip.set_audio(audio_clip)

            # Opsional: Jika ingin menambahkan teks/subtitle langsung ke video,
            # Anda bisa menggunakan TextClip di sini (Memerlukan ImageMagick).

            video_clips.append(video_clip)

    if video_clips:
        print(" Menggabungkan semua adegan menjadi satu video...")
        final_video = concatenate_videoclips(video_clips, method="compose")
        output_video_path = "final_youtube_video.mp4"

        # Render video akhir
        final_video.write_videofile(
            output_video_path,
            fps=24,
            codec="libx264",
            audio_codec="aac"
        )
        print(f" Selesai! Video Anda siap di: {output_video_path}")
    else:
        print("Gagal membuat video karena aset tidak lengkap.")


# ==========================================
# MAIN EXECUTION FLOW
# ==========================================
if __name__ == "__main__":
    # Tentukan topik yang ingin Anda buat videonya hari ini
    TOPIC_TREND = "Perkembangan Artificial Intelligence terbaru di tahun 2026"

    try:
        # 1. Cari Internet
        internet_info = search_latest_trend(TOPIC_TREND)

        # 2. Minta Gemini buat skrip terstruktur (JSON)
        video_script = generate_script_with_gemini(internet_info, TOPIC_TREND)
        print("\nSkrip Berhasil Dibuat oleh Gemini:")
        print(json.dumps(video_script, indent=2, ensure_ascii=False))
        print("\n" + "=" * 40 + "\n")

        # 3, 4, 5. Proses Aset dan Satukan Video
        create_final_video(video_script)

    except Exception as e:
        print(f"Terjadi kesalahan dalam sistem pipeline: {e}")

print("Semua library berhasil terinstall dengan aman!")
