import streamlit as st
import yt_dlp
import os

# --- الإعدادات والواجهة الأصلية 100% ---
st.set_page_config(page_title="YouTube Downloader", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .logo-text { color: #00c6ff; font-size: 25px; font-weight: bold; margin-bottom: 0px; }
    .glow-title { font-size: 60px; font-weight: 900; color: #FFFFFF; text-align: center; margin-top: -20px; }
    .welcome-msg { color: #00c6ff; font-size: 20px; text-align: center; margin-bottom: 40px; font-weight: bold; }
    .footer { color: #666; text-align: center; margin-top: 100px; font-size: 16px; }
    
    /* تنسيق الحقول لتشبه الصورة */
    div.stTextInput > div > div > input { background-color: #f0f2f6; color: #31333F; border-radius: 10px; }
    div.stSelectbox > div > div > div { background-color: #f0f2f6; border-radius: 10px; }
    
    /* تنسيق الزرار */
    div.stButton > button {
        background-color: #000000;
        color: #FFFFFF;
        border: 2px solid #00c6ff;
        border-radius: 20px;
        padding: 5px 25px;
        font-weight: bold;
    }
    div.stButton > button:hover { border-color: #FFFFFF; color: #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# اللوجو والعنوان
st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️ جاهز لتحميل فيديوهاتك المفضلة؟</div>', unsafe_allow_html=True)

# المسار السري للكوكيز
cookie_path = "cookies.txt" if os.path.exists("cookies.txt") else None

# حقل الرابط
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

# منطق جلب الجودات
if url_input:
    try:
        ydl_opts_info = {
            'quiet': True, 
            'cookiefile': cookie_path,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url_input, download=False)
            formats = info.get('formats', [])
            heights = sorted(list(set(f['height'] for f in formats if f.get('height') and f.get('acodec') != 'none')), reverse=True)
            available_qs = [f"{h}p" for h in heights] if heights else ["أفضل جودة"]
            st.session_state.v_title = info.get('title', 'video')
    except:
        available_qs = ["رابط غير صحيح"]

    # تقسيم الاختيارات في صف واحد (زي الصورة)
    col1, col2 = st.columns(2)
    with col1:
        format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
    with col2:
        selected_quality = st.selectbox("🎬 الجودة المتاحة:", available_qs)

    # زرار "ابدأ الآن"
    if st.button("🚀 ابدأ الآن"):
        status = st.empty()
        status.markdown("<h3 style='color: #00c6ff; text-align: center;'>⏳ جاري المعالجة بأقصى سرعة...</h3>", unsafe_allow_html=True)
        
        ext = "mp4" if "فيديو" in format_type else "mp3"
        temp_name = f"video_{st.session_state.v_title}.{ext}".replace(" ", "_")
        
        ydl_opts_dl = {
            'format': f'bestvideo[height<={selected_quality.replace("p","")}][ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': temp_name,
            'cookiefile': cookie_path,
            'nocheckcertificate': True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                ydl.download([url_input])
            
            if os.path.exists(temp_name):
                with open(temp_name, "rb") as f:
                    st.download_button(
                        label="📥 اضغط هنا لحفظ الملف على جهازك",
                        data=f,
                        file_name=f"{st.session_state.v_title}.{ext}",
                        use_container_width=True
                    )
                st.balloons()
                status.empty()
                os.remove(temp_name)
        except Exception as e:
            st.error(f"حدث خطأ: {e}")

# التذييل (Footer)
st.markdown('<div class="footer">El_kasrawy Downloader ❤️</div>', unsafe_allow_html=True)
