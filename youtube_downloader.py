import streamlit as st
import yt_dlp
import os
import time
import uuid
import re

# --- الإعدادات والواجهة ---
st.set_page_config(page_title="YouTube Downloader", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; }
    .glow-title { font-size: 40px; font-weight: 900; color: #FFFFFF; text-align: center; }
    
    div.stButton > button {
        background-color: transparent; color: #00c6ff; border: 2px solid #00c6ff;
        border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
    }
    div.stButton > button:hover { background-color: #00c6ff; color: white; }
    
    div.stDownloadButton > button {
        background-color: #00c6ff !important; 
        color: white !important; 
        border: none !important;
        border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
        font-size: 18px;
    }
    
    .history-card { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

if 'history' not in st.session_state: st.session_state.history = []
if 'video_data' not in st.session_state:
    st.session_state.video_data = {'title': "ابحث عن فيديو", 'thumb': "https://via.placeholder.com/400x225/111/333", 'qs': ["أفضل جودة"]}

st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)

col_input, col_search = st.columns([4, 1])
with col_input:
    url_input = st.text_input("YouTube URL", placeholder="ضع رابط الفيديو هنا...", key="url_bar", label_visibility="collapsed")
with col_search:
    search_btn = st.button("🔍 بحث")

# --- محرك البحث باستخدام الكوكيز ---
if search_btn and url_input:
    try:
        with st.spinner("🔄 جاري فحص الجودات بالهوية الجديدة..."):
            ydl_opts = {
                'quiet': True, 
                'nocheckcertificate': True,
                'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url_input, download=False)
                formats = info.get('formats', [])
                heights = sorted(list(set(f['height'] for f in formats if f.get('height'))), reverse=True)
                st.session_state.video_data = {
                    'title': info.get('title', 'Video'),
                    'thumb': info.get('thumbnail'),
                    'qs': [f"{h}p" for h in heights] if heights else ["أفضل جودة"]
                }
    except Exception as e:
        st.error(f"❌ خطأ: تأكد من رفع ملف cookies.txt | {e}")

# --- تم تعديل العرض هنا ليكون كامل العرض ---
main_col = st.container()

with main_col:
    st.markdown("### 📥 إعدادات التحميل")
    col_m1, col_m2 = st.columns([1, 1.2])
    with col_m1:
        st.image(st.session_state.video_data['thumb'], width='stretch')
    with col_m2:
        st.write(f"**{st.session_state.video_data['title']}**")
        format_choice = st.selectbox("النوع:", ["فيديو (MP4)", "صوت (MP3)"])
        quality_choice = st.selectbox("الجودة:", st.session_state.video_data['qs'])

    progress_bar = st.progress(0)
    status_text = st.empty()

    def progress_hook(d):
        if d['status'] == 'downloading':
            p = d.get('_percent_str', '0%').replace('%','')
            try:
                progress_bar.progress(float(p)/100)
                status_text.text(f"🚀 جاري التحميل: {d.get('_percent_str')}")
            except: pass

    if st.button("🚀 ابدأ التحميل"):
        if url_input:
            is_mp3 = "صوت" in format_choice
            ext = "mp3" if is_mp3 else "mp4"
            unique_id = uuid.uuid4().hex
            out_file = f"{unique_id}.{ext}"
            q_num = quality_choice.replace("p", "")
            
            ydl_opts = {
                # التعديل ده بيضمن دمج الصوت والصورة لأي جودة (بيحتاج ffmpeg في ملف packages.txt)
                'format': f'bestvideo[ext=mp4][height<={q_num}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': out_file,
                'merge_output_format': 'mp4' if not is_mp3 else None,
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True,
                #تسجيل الهوية لتخطي الحظر
                'username': 'oauth2',
                'password': '',
                # --- إعدادات إضافية لزيادة الموثوقية ---
                # 'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'user_agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36',
                'http_headers': {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                    },
                'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
                'quiet': True
            }
            if is_mp3:
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                if os.path.exists(out_file):
                    # إضافة الفيديو للسجل عند النجاح
                    st.session_state.history.append({"title": st.session_state.video_data['title']})
                    
                    status_text.text("✅ تمت المعالجة! اضغط على الزر الأزرق")
                    with open(out_file, "rb") as f:
                        st.download_button(
                            label="📥 حفظ الملف الآن",
                            data=f,
                            file_name=f"video_{unique_id}.{ext}",
                            mime="video/mp4" if not is_mp3 else "audio/mpeg"
                        )
                else: st.error("❌ فشل التحميل")
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

# --- التعديل السحري هنا: السجل في القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("### 📜 السجل")
    if st.button("🗑️ مسح السجل"):
        st.session_state.history = []
        st.rerun()
    
    for item in reversed(st.session_state.history):
        st.markdown(f'<div class="history-card"><b>{item["title"][:30]}</b></div>', unsafe_allow_html=True)

st.markdown("<br><center>El_kasrawy Pro 2025</center>", unsafe_allow_html=True)

