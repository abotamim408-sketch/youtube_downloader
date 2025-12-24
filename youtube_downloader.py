import streamlit as st
import yt_dlp
import os
import time
import shutil  # لنقل الملفات تلقائياً
import uuid    # لإنشاء أسماء ملفات مؤقتة فريدة
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
    .history-card { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00c6ff; }
    </style>
    """, unsafe_allow_html=True)

# تهيئة السجل وحالة الفيديو
if 'history' not in st.session_state: st.session_state.history = []
if 'video_data' not in st.session_state:
    st.session_state.video_data = {'title': "ابحث عن فيديو", 'thumb': "https://via.placeholder.com/400x225/111/333", 'qs': ["أفضل جودة"]}

# --- الهيدر ---
st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader  🎬</div>', unsafe_allow_html=True)

# --- 1. منطقة البحث ---
col_input, col_search = st.columns([4, 1])
with col_input:
    url_input = st.text_input("", placeholder="ضع رابط الفيديو هنا...", key="url_bar", label_visibility="collapsed")
with col_search:
    search_btn = st.button("🔍 بحث")

if search_btn and url_input:
    try:
        with st.spinner("🔄 جاري فحص الجودات..."):
            ydl_opts = {'quiet': True, 'nocheckcertificate': True}
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
        st.error(f"❌ خطأ: {e}")

# --- تقسيم الشاشة ---
main_col, side_col = st.columns([2, 1])

with main_col:
    st.markdown("### 📥 إعدادات التحميل")
    col_m1, col_m2 = st.columns([1, 1.2])
    with col_m1:
        st.image(st.session_state.video_data['thumb'], use_container_width=True)
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
                status_text.text(f"🚀 جاري التحميل: {d.get('_percent_str')} | السرعة: {d.get('_speed_str')}")
            except: pass
        if d['status'] == 'finished':
            status_text.text("✅ اكتمل التحميل، يتم الحفظ التلقائي الآن...")

    if st.button("🚀 ابدأ التحميل الآن"):
        if url_input:
            is_mp3 = "صوت" in format_choice
            ext = "mp3" if is_mp3 else "mp4"
            
            # مجلد مؤقت للتحميل
            temp_dir = "temp_dl"
            if not os.path.exists(temp_dir): os.makedirs(temp_dir)
            
            # تنظيف اسم الملف
            safe_title = re.sub(r'[\\/*?:"<>|]', "", st.session_state.video_data['title'])
            unique_name = f"dl_{uuid.uuid4().hex}"
            temp_out_path = os.path.join(temp_dir, f"{unique_name}.%(ext)s")
            
            q_num = quality_choice.replace("p", "")
            
            # إعدادات مرنة للجودة لتفادي أخطاء Format not available
            if is_mp3:
                f_spec = 'bestaudio/best'
            else:
                f_spec = f'bestvideo[height<={q_num}][ext=mp4]+bestaudio[ext=m4a]/best[height<={q_num}]/best' if q_num != "أفضل جودة" else 'bestvideo+bestaudio/best'

            ydl_opts = {
                'format': f_spec,
                'outtmpl': temp_out_path,
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True,
                'quiet': True
            }
            if is_mp3:
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                # تحديد مسار Downloads الخاص بالمستخدم
                user_downloads = os.path.join(os.path.expanduser("~"), "Downloads")
                final_filename = f"{safe_title}.{ext}"
                final_path = os.path.join(user_downloads, final_filename)

                # البحث عن الملف الفعلي الذي تم تحميله في المجلد المؤقت
                downloaded_file = None
                for f in os.listdir(temp_dir):
                    if f.startswith(unique_name):
                        downloaded_file = os.path.join(temp_dir, f)
                        break

                if downloaded_file:
                    shutil.move(downloaded_file, final_path) # النقل التلقائي
                    
                    # إضافة للسجل
                    st.session_state.history.append({"title": safe_title, "time": time.strftime("%H:%M:%S"), "ext": ext})
                    st.success(f"✅ تم الحفظ تلقائياً في مجلد Downloads باسم: {final_filename}")
                else:
                    st.error("❌ تعذر العثور على الملف بعد تحميله.")
            except Exception as e:
                st.error(f"❌ خطأ أثناء التحميل: {e}")

with side_col:
    st.markdown("### 📜 السجل (History)")
    if not st.session_state.history:
        st.write("لا يوجد عمليات تحميل سابقة")
    else:
        if st.button("🗑️ مسح السجل"):
            st.session_state.history = []
            st.rerun()
        for item in reversed(st.session_state.history):
            st.markdown(f'<div class="history-card"><small style="color:#00c6ff;">{item["time"]}</small><br><b>{item["title"][:30]}...</b><br><small>Type: {item["ext"].upper()}</small></div>', unsafe_allow_html=True)

st.markdown("<br><center style='color:#444;'>El_kasrawy Downloader Pro © 2025</center>", unsafe_allow_html=True)
