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
    
    /* تنسيق زر التحميل النهائي ليكون أزرق وواضح */
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

if search_btn and url_input:
    try:
        with st.spinner("🔄 جاري فحص الجودات..."):
            # إعدادات لتجنب حظر 403
            ydl_opts = {
                'quiet': True, 
                'nocheckcertificate': True,
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
        st.error(f"❌ خطأ في فحص الرابط: {e}")

main_col, side_col = st.columns([2, 1])

with main_col:
    st.markdown("### 📥 إعدادات التحميل")
    col_m1, col_m2 = st.columns([1, 1.2])
    with col_m1:
        # تحديث التحذير الخاص بـ use_container_width
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

    if st.button("🚀 ابدأ المعالجة الآن"):
        if url_input:
            is_mp3 = "صوت" in format_choice
            ext = "mp3" if is_mp3 else "mp4"
            safe_title = re.sub(r'[\\/*?:"<>|]', "", st.session_state.video_data['title'])
            unique_id = uuid.uuid4().hex
            out_file = f"{unique_id}.{ext}"
            q_num = quality_choice.replace("p", "")
            
            # إعدادات مكثفة لتخطي حماية يوتيوب 403
            ydl_opts = {
                'format': f'bestvideo[height<={q_num}]+bestaudio/best' if not is_mp3 else 'bestaudio/best',
                'outtmpl': out_file,
                'merge_output_format': 'mp4' if not is_mp3 else None,
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'referer': 'https://www.google.com/',
                'http_chunk_size': 1048576,
            }
            if is_mp3:
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                if os.path.exists(out_file):
                    status_text.text("✅ تمت المعالجة بنجاح")
                    with open(out_file, "rb") as f:
                        st.download_button(
                            label="📥 اضغط هنا لحفظ الملف الآن",
                            data=f,
                            file_name=f"{safe_title}.{ext}",
                            mime="video/mp4" if not is_mp3 else "audio/mpeg"
                        )
                    st.session_state.history.append({"title": safe_title, "time": time.strftime("%H:%M:%S")})
                else:
                    st.error("❌ فشل تحميل الملف.")
            except Exception as e:
                st.error(f"❌ خطأ: {e}")

with side_col:
    st.markdown("### 📜 السجل (History)")
    for item in reversed(st.session_state.history):
        st.markdown(f'<div class="history-card"><small>{item["time"]}</small><br><b>{item["title"][:30]}...</b></div>', unsafe_allow_html=True)
