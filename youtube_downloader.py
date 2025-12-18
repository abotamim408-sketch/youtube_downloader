import streamlit as st
import yt_dlp
import os

# --- الإعدادات ---
st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); }
    .glow-title { font-size: 50px; font-weight: 900; color: #FFFFFF; text-align: center; text-shadow: 0 0 15px rgba(0, 198, 255, 0.9); }
    .welcome-msg { color: #00c6ff; font-size: 19px; text-align: center; margin-bottom: 30px; }
    div.stButton > button { width: 100%; border-radius: 50px; border: 2px solid #00c6ff; background: transparent; color: white; font-size: 20px; }
    div.stButton > button:hover { background: #00c6ff; color: black; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️ جاهز للتحميل؟</div>', unsafe_allow_html=True)

url_input = st.text_input("🔗 ضع رابط الفيديو هنا:")

if url_input:
    format_type = st.selectbox("📦 النوع:", ["فيديو (MP4)", "صوت (MP3)"])
    
    if st.button("🚀 ابدأ التحميل الآن"):
        with st.spinner("⏳ جاري المعالجة... قد يستغرق ذلك دقيقة"):
            # تحديد اسم ملف مؤقت بسيط بدون مسارات معقدة
            out_file = "video_temp.mp4" if "فيديو" in format_type else "audio_temp.mp3"
            
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best' if "فيديو" in format_type else 'bestaudio/best',
                'outtmpl': out_file,
                'noplaylist': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                # إظهار زرار التحميل للجهاز
                if os.path.exists(out_file):
                    with open(out_file, "rb") as f:
                        st.download_button(
                            label="✅ اضغط هنا لحفظ الملف على جهازك",
                            data=f,
                            file_name=out_file,
                            mime="video/mp4" if "فيديو" in format_type else "audio/mpeg"
                        )
                    os.remove(out_file) # مسح الملف المؤقت
                else:
                    st.error("❌ عذراً، لم يتم العثور على الملف المحمل.")
            except Exception as e:
                st.error(f"⚠️ فشل: {e}")

st.markdown('<div style="color: #666; text-align: center; margin-top: 50px;">El_kasrawy Downloader ❤️</div>', unsafe_allow_html=True)

