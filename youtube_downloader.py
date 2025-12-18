import streamlit as st
import yt_dlp
import os
import time

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="El_kasrawy Downloader", layout="centered")

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); }
    .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; text-align: left; margin-bottom: 10px; }
    .glow-title {
        font-size: 50px; font-weight: 900; color: #FFFFFF; text-align: center;
        text-shadow: 0 0 15px rgba(0, 198, 255, 0.9);
        margin-bottom: 10px;
    }
    .welcome-msg { color: #00c6ff; font-size: 19px; font-weight: 500; text-align: center; margin-bottom: 30px; }
    
    div.stButton > button {
        width: 100%; padding: 12px 40px !important; font-size: 20px !important;
        font-weight: bold !important; border-radius: 50px !important;
        border: 2px solid #00c6ff !important; background-color: transparent !important;
        color: #FFFFFF !important; transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #00c6ff !important; color: #000 !important;
        box-shadow: 0 0 20px #00c6ff;
    }
    .goodbye-msg { color: #666; font-size: 14px; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. رسالة الترحيب ---
st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️! جاهز لتحميل فيديوهاتك المفضلة؟ </div>', unsafe_allow_html=True)

# --- 3. جلب بيانات الفيديو ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

available_qualities = []
v_title = "video"

if url_input:
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'nocheckcertificate': True}) as ydl:
            info = ydl.extract_info(url_input, download=False)
            v_title = info.get('title', 'video')
            formats = info.get('formats', [])
            # فلترة الجودات المدمجة الجاهزة
            heights = sorted(list(set(f['height'] for f in formats if f.get('height') and f.get('acodec') != 'none')), reverse=True)
            available_qualities = [f"{h}p" for h in heights]
            if not available_qualities: available_qualities = ["أفضل جودة متاحة"]
    except:
        available_qualities = ["رابط غير صحيح"]

# --- 4. الاختيارات ---
c1, c2 = st.columns(2)
with c1:
    format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
with c2:
    selected_quality = st.selectbox("🎬 الجودة المتاحة:", available_qualities if url_input else ["أدخل الرابط أولاً"])

# --- 5. عملية التحميل ---
if st.button("🚀 ابدأ الآن"):
    if not url_input or "أدخل" in selected_quality:
        st.warning("برجاء إدخال رابط صحيح")
    else:
        with st.spinner("⏳ جاري التحميل... برجاء الانتظار"):
            ext = "mp4" if "فيديو" in format_type else "mp3"
            # تنظيف عنوان الفيديو من أي رموز غريبة قد تسبب خطأ
            clean_title = "".join([c for c in v_title if c.isalnum() or c in (' ', '.', '_')]).rstrip()
            final_filename = f"{clean_title}.{ext}"
            
            q_id = selected_quality.replace("p","")
            ydl_opts = {
                'format': f'best[height<={q_id}][ext=mp4]/best' if ext == "mp4" else 'bestaudio/best',
                'outtmpl': final_filename,
                'nocheckcertificate': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                if os.path.exists(final_filename):
                    with open(final_filename, "rb") as f:
                        st.download_button(
                            label="✅ اضغط هنا لحفظ الملف على جهازك",
                            data=f,
                            file_name=final_filename,
                            mime="video/mp4" if ext == "mp4" else "audio/mpeg",
                            use_container_width=True
                        )
                    st.balloons()
                    # حذف الملف من السيرفر فوراً لضمان عدم حدوث تداخل مستقبلاً
                    os.remove(final_filename)
                else:
                    st.error("عذراً، حدث خطأ في إنشاء الملف. حاول مرة أخرى.")
            except Exception as e:
                st.error(f"⚠️ فشل التحميل: {e}")

# --- 6. رسالة الوداع ---
st.markdown('<div class="goodbye-msg">شكراً لاستخدامك El_kasrawy Downloader.. نتمنى لك يوماً سعيداً! ❤️</div>', unsafe_allow_html=True)
