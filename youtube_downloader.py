
import streamlit as st
import yt_dlp
import os

# --- واجهتك الأصلية 100% ---
st.set_page_config(page_title="YouTube Downloader", layout="centered")

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
st.markdown('<div class="welcome-msg">مرحباً بك ❤️ جاهز لتحميل فيديوهاتك المفضلة؟</div>', unsafe_allow_html=True)

# التأكد من مسار الكوكيز بدقة
cookie_path = os.path.join(os.getcwd(), "cookies.txt")
cookie_exists = os.path.exists(cookie_path)

url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

if url_input:
    try:
        ydl_opts_info = {
            'quiet': True,
            'cookiefile': cookie_path if cookie_exists else None,
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'nocheckcertificate': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(url_input, download=False)
            formats = info.get('formats', [])
            heights = sorted(list(set(f['height'] for f in formats if f.get('height') and f.get('acodec') != 'none')), reverse=True)
            available_qs = [f"{h}p" for h in heights] if heights else ["أفضل جودة متاحة"]
            st.session_state.v_title = info.get('title', 'video')
            st.session_state.qs = available_qs
    except Exception as e:
        st.session_state.qs = ["رابط غير صحيح أو محمي"]

    c1, c2 = st.columns(2)
    with c1: format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
    with c2: selected_quality = st.selectbox("🎬 الجودة المتاحة:", st.session_state.get('qs', ["انتظر..."]))

    if st.button("🚀 ابدأ الآن"):
        msg = st.empty()
        msg.markdown("<h4 style='color: #00c6ff; text-align: center;'>⏳ جاري المعالجة بأقصى سرعة...</h4>", unsafe_allow_html=True)
        
        ext = "mp4" if "فيديو" in format_type else "mp3"
        temp_name = f"video_{os.getpid()}.{ext}" # اسم فريد للملف
        
        q_id = selected_quality.replace("p","")
        ydl_opts_dl = {
            'format': f'bestvideo[height<={q_id}][ext=mp4]+bestaudio[ext=m4a]/best[height<={q_id}]',
            'outtmpl': temp_name,
            'cookiefile': cookie_path if cookie_exists else None,
            'nocheckcertificate': True,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts_dl) as ydl:
                ydl.download([url_input])
            
            if os.path.exists(temp_name) and os.path.getsize(temp_name) > 0:
                with open(temp_name, "rb") as f:
                    st.download_button("📥 اضغط هنا لحفظ الملف فوراً", f, file_name=f"{st.session_state.v_title}.{ext}", use_container_width=True)
                st.success("✅ تم التجهيز!")
                st.balloons()
                msg.empty()
                os.remove(temp_name)
            else:
                st.error("فشل التحميل: يرجى تحديث ملف cookies.txt في GitHub")
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)[:100]}")

st.markdown('<div style="color: #666; text-align: center; margin-top: 50px;"> ❤️شكرا لاستخدامك موقعنا , نتمنى لك يوما سعيدا </div>', unsafe_allow_html=True)

