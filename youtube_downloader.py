import streamlit as st
import yt_dlp
import os

# --- 1. الإعدادات والتصميم (نفس الستايل الخاص بك) ---
st.set_page_config(page_title="El_kasrawy Downloader", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); }
    .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; text-align: left; }
    .glow-title { font-size: 50px; font-weight: 900; color: #FFFFFF; text-align: center; text-shadow: 0 0 15px rgba(0, 198, 255, 0.9); }
    .welcome-msg { color: #00c6ff; font-size: 19px; text-align: center; margin-bottom: 30px; }
    div.stButton > button { width: 100%; border-radius: 50px; border: 2px solid #00c6ff; background: transparent; color: white; font-size: 20px; font-weight: bold; }
    div.stButton > button:hover { background: #00c6ff; color: black; box-shadow: 0 0 20px #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️ جاهز للتحميل؟</div>', unsafe_allow_html=True)

# --- 4. الواجهة (نفس كودك بالظبط) ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

if "available_qs" not in st.session_state:
    st.session_state.available_qs = ["أدخل الرابط أولاً"]

if url_input:
    try:
        # إضافة User-Agent لحل مشكلة No supported JavaScript runtime
        ydl_opts_info = {
            'quiet': True, 
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url_input, download=False)
            formats = info.get('formats', [])
            # جلب الجودات المدمجة الجاهزة لتجنب خطأ ffmpeg
            heights = sorted(list(set(f['height'] for f in formats if f.get('height') and f.get('acodec') != 'none')), reverse=True)
            st.session_state.available_qs = [f"{h}p" for h in heights] if heights else ["أفضل جودة متاحة"]
            st.session_state.v_title = info.get('title', 'Video')
    except:
        st.session_state.available_qs = ["رابط غير صحيح"]

c1, c2 = st.columns(2)
with c1:
    format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
with c2:
    selected_quality = st.selectbox("🎬 الجودة المتاحة:", st.session_state.available_qs)

path_input = st.text_input("📂 مكان الحفظ:", value=os.path.join(os.getcwd(), "downloads"))

# --- 5. التحميل ---
if st.button("🚀 ابدأ الآن"):
    if url_input and "p" in selected_quality or "أفضل" in selected_quality:
        progress_bar_place = st.empty()
        progress_bar_place.markdown("<h4 style='color: #00c6ff; text-align: center;'>⏳ جاري التحميل... برجاء الانتظار</h4>", unsafe_allow_html=True)
        
        q_id = selected_quality.replace("p","")
        temp_filename = "downloaded_video.mp4" if "فيديو" in format_type else "downloaded_audio.mp3"
        
        if os.path.exists(temp_filename): os.remove(temp_filename)

        ydl_opts_dl = {
            # اختيار صيغة مدمجة جاهزة لتجنب إيرور Empty File
            'format': f'best[height<={q_id}][ext=mp4]/best' if "فيديو" in format_type else 'bestaudio/best',
            'outtmpl': temp_filename,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                ydl.download([url_input])
            
            if os.path.exists(temp_filename) and os.path.getsize(temp_filename) > 0:
                with open(temp_filename, "rb") as f:
                    st.download_button(
                        label="✅ اضغط هنا لحفظ الملف على جهازك",
                        data=f,
                        file_name=f"{st.session_state.v_title}.{'mp4' if 'فيديو' in format_type else 'mp3'}",
                        mime="video/mp4" if "فيديو" in format_type else "audio/mpeg",
                        use_container_width=True
                    )
                st.balloons()
                progress_bar_place.empty()
            else:
                st.error("ERROR: The downloaded file is empty")
        except Exception as e:
            st.error(f"فشل التحميل: {e}")

st.markdown('<div style="color: #666; text-align: center; margin-top: 50px;">El_kasrawy Downloader ❤️</div>', unsafe_allow_html=True)
