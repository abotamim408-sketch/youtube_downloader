import streamlit as st
import yt_dlp
import os

# --- 1. التصميم (نفس الستايل الخاص بك 100%) ---
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

# --- 2. الواجهة ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

if "available_qs" not in st.session_state:
    st.session_state.available_qs = ["أدخل الرابط أولاً"]

if url_input:
    try:
        # إضافة إعدادات متقدمة لتجنب حظر يوتيوب
        ydl_opts_info = {
            'quiet': True, 'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url_input, download=False)
            formats = info.get('formats', [])
            # جلب الجودات التي تدعم الصوت والصورة معاً لتجنب مشاكل الدمج
            heights = sorted(list(set(f['height'] for f in formats if f.get('height') and f.get('acodec') != 'none')), reverse=True)
            st.session_state.available_qs = [f"{h}p" for h in heights] if heights else ["أفضل جودة متاحة"]
            st.session_state.v_title = info.get('title', 'Video')
    except:
        st.session_state.available_qs = ["رابط غير صحيح"]

c1, c2 = st.columns(2)
with c1: format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
with c2: selected_quality = st.selectbox("🎬 الجودة المتاحة:", st.session_state.available_qs)

path_input = st.text_input("📂 مكان الحفظ (للعرض فقط):", value="/mount/src/youtube_downloader/downloads")

# --- 3. التحميل ---
if st.button("🚀 ابدأ الآن"):
    if url_input and ("p" in selected_quality or "أفضل" in selected_quality):
        msg = st.empty()
        msg.markdown("<h4 style='color: #00c6ff; text-align: center;'>⏳ جاري معالجة الفيديو... برجاء الانتظار</h4>", unsafe_allow_html=True)
        
        q_id = selected_quality.replace("p","")
        # اسم ملف ثابت مؤقت لضمان القراءة الصحيحة
        temp_fn = "final_output.mp4" if "فيديو" in format_type else "final_output.mp3"
        if os.path.exists(temp_fn): os.remove(temp_fn)

        ydl_opts_dl = {
            # اختيار جودة مدمجة (فيديو+صوت) لتجنب خطأ الدمج اللي ظهر عندك
            'format': f'bestvideo[height<={q_id}][ext=mp4]+bestaudio[ext=m4a]/best[height<={q_id}]/best',
            'outtmpl': temp_fn,
            'nocheckcertificate': True,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/119.0.0.0 Safari/537.36'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                ydl.download([url_input])
            
            if os.path.exists(temp_fn) and os.path.getsize(temp_fn) > 0:
                with open(temp_fn, "rb") as f:
                    st.download_button(
                        label="✅ اضغط هنا لحفظ الملف على جهازك",
                        data=f,
                        file_name=f"{st.session_state.v_title}.{'mp4' if 'فيديو' in format_type else 'mp3'}",
                        mime="video/mp4" if "فيديو" in format_type else "audio/mpeg",
                        use_container_width=True
                    )
                st.balloons()
                msg.empty()
            else:
                st.error("فشل التحميل: الملف الناتج فارغ، جرب جودة أقل (مثل 720p).")
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

st.markdown('<div style="color: #666; text-align: center; margin-top: 50px;">El_kasrawy Downloader ❤️</div>', unsafe_allow_html=True)
