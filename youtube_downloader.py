import streamlit as st
import yt_dlp
import os
import time

# --- 1. الإعدادات والتصميم ---
st.set_page_config(page_title="YouTube Downloader", layout="centered")

if 'history' not in st.session_state: st.session_state.history = []
if 'available_qs' not in st.session_state: st.session_state.available_qs = ["أدخل الرابط أولاً"]

st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); }
    
    /* اللوجو في الجنب كما طلبت */
    .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; text-align: left; margin-bottom: 10px; }
    
    /* العنوان الرئيسي */
    .glow-title {
        font-size: 50px; font-weight: 900; color: #FFFFFF; text-align: center;
        text-shadow: 0 0 15px rgba(0, 198, 255, 0.9);
        margin-bottom: 10px;
    }
    
    /* رسالة الترحيب بخط معدول */
    .welcome-msg { color: #00c6ff; font-size: 19px; font-weight: 500; text-align: center; margin-bottom: 30px; }

    /* --- التعديل الجوهري لتوسيط الزرار في نص المربع بالظبط --- */
    .stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    div.stButton > button {
        padding: 12px 40px !important;
        font-size: 20px !important;
        font-weight: bold !important;
        border-radius: 50px !important;
        border: 2px solid #00c6ff !important;
        background-color: transparent !important;
        color: #FFFFFF !important;
        transition: 0.3s;
    }
    
    div.stButton > button:hover {
        background-color: #00c6ff !important;
        color: #000 !important;
        box-shadow: 0 0 20px #00c6ff;
    }

    /* تنسيق المدخلات */
    div[data-baseweb="input"], div[data-baseweb="select"] { background-color: #FFFFFF !important; border-radius: 12px; border: 2px solid #00c6ff !important; }
    input { color: #000000 !important; font-weight: 600; }
    label { color: #FFFFFF !important; font-weight: bold; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #00c6ff, #0072ff) !important; }
    .goodbye-msg { color: #666; font-size: 14px; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. العناصر العلوية ---
st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)
st.markdown('<div class="welcome-msg">مرحباً بك ❤️! جاهز لتحميل فيديوهاتك المفضلة؟ </div>', unsafe_allow_html=True)

# --- 3. دالة التقدم ---
def progress_hook(d):
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%','')
        try:
            progress_bar_place.progress(float(p)/100, text=f"⏳ جاري التحميل الآن... {p}%")
        except: pass
    elif d['status'] == 'finished':
        progress_bar_place.markdown("<h4 style='color: #28a745; text-align: center;'>✅ اكتمل التحميل بنجاح!</h4>", unsafe_allow_html=True)

# --- 4. الواجهة ---
url_input = st.text_input("🔗 ضع رابط الفيديو هنا:", placeholder="https://youtube.com/...")

if url_input:
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'nocheckcertificate': True}) as ydl:
            info = ydl.extract_info(url_input, download=False)
            formats = info.get('formats', [])
            heights = sorted(list(set(f['height'] for f in formats if f.get('height'))), reverse=True)
            st.session_state.available_qs = [f"{h}p" for h in heights]
            st.session_state.v_title = info.get('title', 'Video')
    except:
        st.session_state.available_qs = ["رابط غير صحيح"]

c1, c2 = st.columns(2)
with c1:
    format_type = st.selectbox("📦 نوع الملف:", ["فيديو (MP4)", "صوت (MP3)"])
with c2:
    selected_quality = st.selectbox("🎬 الجودة:", st.session_state.available_qs)

path_input = st.text_input("📂 مكان الحفظ:", value=os.path.join(os.getcwd(), "downloads"))

# --- 5. التحميل ---
st.write("") 
download_btn = st.button("🚀 ابدأ الآن")
progress_bar_place = st.empty()

if download_btn:
    if url_input and "p" in selected_quality:
        progress_bar_place.markdown("<h4 style='color: #00c6ff; text-align: center;'>⏳ جاري معالجة الفيديو... برجاء الانتظار</h4>", unsafe_allow_html=True)
        
        q_id = selected_quality.replace("p","")
        # تعديل اسم الملف ليكون مؤقت وبسيط
        temp_filename = "downloaded_video.mp4" if "فيديو" in format_type else "downloaded_audio.mp3"
        
        ydl_opts = {
            'format': f'best[height<={q_id}][ext=mp4]/best' if "فيديو" in format_type else 'bestaudio/best',
            'outtmpl': temp_filename,  # الحفظ في الملف المؤقت
            'nocheckcertificate': True,
            'quiet': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url_input])
            
            # --- الخطوة الأهم: إرسال الملف للمستخدم ---
            with open(temp_filename, "rb") as f:
                st.download_button(
                    label="✅ اضغط هنا لحفظ الملف على جهازك",
                    data=f,
                    file_name=f"{st.session_state.get('v_title', 'video')}.{'mp4' if 'فيديو' in format_type else 'mp3'}",
                    mime="video/mp4" if "فيديو" in format_type else "audio/mpeg",
                    use_container_width=True
                )
            st.balloons()
            # مسح الملف من السيرفر بعد التحميل لتوفير المساحة
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
                
        except Exception as e:
            st.error(f"⚠️ فشل التحميل: {e}")

# --- 6. السجل والوداع ---
st.markdown('<div class="goodbye-msg">شكراً لاستخدامك El_kasrawy Downloader.. نتمنى لك يوماً سعيداً! ❤️</div>', unsafe_allow_html=True)
