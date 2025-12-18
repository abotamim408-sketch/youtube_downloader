import streamlit as st
import yt_dlp
import os

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="El_kasrawy Downloader", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); }
    .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; text-align: left; }
    .glow-title {
        font-size: 45px; font-weight: 900; color: #FFFFFF; text-align: center;
        text-shadow: 0 0 15px rgba(0, 198, 255, 0.9);
    }
    .welcome-msg { color: #00c6ff; font-size: 18px; text-align: center; margin-bottom: 30px; }
    
    /* تنسيق زرار التحميل */
    div.stButton > button {
        width: 100%;
        padding: 12px !important;
        font-size: 20px !important;
        border-radius: 50px !important;
        border: 2px solid #00c6ff !important;
        background: transparent !important;
        color: white !important;
    }
    div.stButton > button:hover {
        background: #00c6ff !important;
        color: black !important;
        box-shadow: 0 0 20px #00c6ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️ جاهز لتحميل فيديوهاتك؟ </div>', unsafe_allow_html=True)

# --- 2. مدخلات المستخدم ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")
format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])

# --- 3. معالجة التحميل ---
if st.button("🚀 ابدأ التحميل الآن"):
    if not url_input:
        st.warning("رجاءً ضع رابط الفيديو أولاً!")
    else:
        with st.spinner("⏳ جاري التحميل والمعالجة... قد يستغرق ذلك دقيقة"):
            # اسم ملف مؤقت بسيط
            ext = "mp4" if "فيديو" in format_type else "mp3"
            out_file = f"video_download.{ext}"
            
            ydl_opts = {
                # اختيار أفضل جودة مدمجة جاهزة لتجنب خطأ ffmpeg
                'format': 'best[ext=mp4]/best' if "فيديو" in format_type else 'bestaudio/best',
                'outtmpl': out_file,
                'noplaylist': True,
                'nocheckcertificate': True,
            }

            try:
                if os.path.exists(out_file):
                    os.remove(out_file) # تنظيف أي ملف قديم
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                # --- 4. زرار الحفظ النهائي على الجهاز ---
                if os.path.exists(out_file):
                    with open(out_file, "rb") as f:
                        st.download_button(
                            label="✅ اضغط هنا لحفظ الملف على جهازك",
                            data=f,
                            file_name=out_file,
                            mime="video/mp4" if ext=="mp4" else "audio/mpeg",
                            use_container_width=True
                        )
                    st.balloons()
                    # ملاحظة: سيتم حذف الملف عند تحديث الصفحة أو انتهاء الجلسة
                else:
                    st.error("فشل في العثور على الملف بعد التحميل.")
            except Exception as e:
                st.error(f"⚠️ حدث خطأ: {e}")

st.markdown('<div style="color: #666; text-align: center; margin-top: 50px;">El_kasrawy Downloader ❤️</div>', unsafe_allow_html=True)
