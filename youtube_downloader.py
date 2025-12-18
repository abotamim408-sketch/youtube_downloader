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
    div.stButton > button {
        width: 100%; padding: 12px !important; font-size: 20px !important;
        border-radius: 50px !important; border: 2px solid #00c6ff !important;
        background: transparent !important; color: white !important;
    }
    div.stButton > button:hover {
        background: #00c6ff !important; color: black !important;
        box-shadow: 0 0 20px #00c6ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)

# --- 2. معالجة الرابط والجودات ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:")

available_qualities = []
video_title = "video"

if url_input:
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url_input, download=False)
            video_title = info.get('title', 'video')
            formats = info.get('formats', [])
            # استخراج الجودات الفريدة التي تحتوي على فيديو وصوت معاً لتجنب مشاكل ffmpeg
            heights = set()
            for f in formats:
                if f.get('height') and f.get('acodec') != 'none' and f.get('vcodec') != 'none':
                    heights.add(f.get('height'))
            
            available_qualities = sorted([f"{h}p" for h in heights], key=lambda x: int(x[:-1]), reverse=True)
            
            if not available_qualities: # حل احتياطي لو ملقاش جودات مدمجة
                available_qualities = ["أفضل جودة متاحة"]
    except:
        st.error("❌ الرابط غير صحيح أو الفيديو غير متاح")

# --- 3. خيارات المستخدم ---
col1, col2 = st.columns(2)
with col1:
    format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
with col2:
    selected_quality = st.selectbox("🎬 الجودة المتاحة:", available_qualities if available_qualities else ["في انتظار الرابط..."])

# --- 4. التحميل ---
if st.button("🚀 ابدأ التحميل الآن"):
    if not url_input or "انتظار" in selected_quality:
        st.warning("رجاءً ضع رابطاً صالحاً أولاً!")
    else:
        with st.spinner("⏳ جاري التحميل..."):
            ext = "mp4" if "فيديو" in format_type else "mp3"
            out_file = f"download.{ext}"
            
            # إعداد الكود ليختار الجودة المحددة
            q_id = selected_quality.replace("p", "")
            ydl_opts = {
                'format': f'best[height<={q_id}][ext=mp4]/best' if ext == "mp4" else 'bestaudio/best',
                'outtmpl': out_file,
                'nocheckcertificate': True,
            }

            try:
                if os.path.exists(out_file): os.remove(out_file)
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                if os.path.exists(out_file):
                    with open(out_file, "rb") as f:
                        st.download_button(
                            label="✅ اضغط هنا لحفظ الملف على جهازك",
                            data=f,
                            file_name=f"{video_title}.{ext}",
                            mime="video/mp4" if ext == "mp4" else "audio/mpeg"
                        )
                    st.balloons()
            except Exception as e:
                st.error(f"⚠️ فشل التحميل: {e}")
