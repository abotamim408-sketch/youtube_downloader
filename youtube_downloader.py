import streamlit as st
import yt_dlp
import os
import time
import re

# --- 1. إعدادات الصفحة وتفعيل السجل في ذاكرة المتصفح ---
st.set_page_config(page_title="El_kasrawy Downloader", layout="wide")

if 'history' not in st.session_state:
    st.session_state.history = []

# --- 2. تنسيق الألوان (حل مشكلة الزر الأبيض) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0e14; color: white; }
    div.stDownloadButton > button {
        background-color: #00c6ff !important;
        color: white !important;
        font-weight: bold;
        border-radius: 10px;
        width: 100%;
        height: 3.5em;
    }
    .history-card {
        background: rgba(255,255,255,0.05);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 5px;
        border-right: 4px solid #00c6ff;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎬 YouTube Downloader Pro")
url = st.text_input("انسخ رابط الفيديو هنا:", placeholder="https://youtube.com/...")

# --- 3. محرك التحميل ---
if st.button("🚀 ابدأ معالجة الفيديو"):
    if url:
        with st.spinner("جاري التحميل..."):
            # تنظيف اسم الفيديو من الرموز الغريبة
            out_file = "video_download.mp4"
            
            ydl_opts = {
                'format': 'best',
                'cookiefile': 'cookies.txt', # التأكد من رفع ملف الكوكيز
                'outtmpl': out_file,
                'nocheckcertificate': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
            }
            
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    video_title = info.get('title', 'Video')
                
                if os.path.exists(out_file):
                    st.success("✅ تمت المعالجة!")
                    
                    # --- إضافة الفيديو للسجل هنا ---
                    st.session_state.history.append({
                        "title": video_title,
                        "time": time.strftime("%H:%M:%S")
                    })
                    
                    with open(out_file, "rb") as file:
                        st.download_button(
                            label="📥 اضغط هنا لتحميل الملف",
                            data=file,
                            file_name=f"{video_title}.mp4",
                            mime="video/mp4"
                        )
            except Exception as e:
                # عرض الخطأ إذا فشل (مثل 403 Forbidden)
                st.error(f"❌ خطأ: {e}")
    else:
        st.warning("⚠️ ضع الرابط أولاً")

# --- 4. عرض السجل في القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.markdown("### 📜 سجل التحميلات")
    if not st.session_state.history:
        st.write("لا يوجد تحميلات بعد")
    else:
        if st.button("🗑️ مسح السجل"):
            st.session_state.history = []
            st.rerun()
        
        for item in reversed(st.session_state.history):
            st.markdown(f"""
            <div class="history-card">
                <small style="color:#00c6ff;">{item['time']}</small><br>
                <b>{item['title'][:40]}...</b>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<br><center style='color:#444;'>El_kasrawy 2025</center>", unsafe_allow_html=True)
