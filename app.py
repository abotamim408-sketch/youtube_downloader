# import streamlit as st
# import yt_dlp
# import os
# import time
# import uuid
# import re
# import config # استيراد ملف الإعدادات اللي عملناه فوق

# # 1. استدعاء التنسيقات من ملف config
# config.apply_custom_styles()

# # 2. تهيئة مخزن البيانات (Session State) للحفاظ على السجل وبيانات الفيديو عند إعادة تحميل الصفحة
# if 'history' not in st.session_state: st.session_state.history = []
# if 'video_data' not in st.session_state:
#     st.session_state.video_data = {'title': "ابحث عن فيديو", 'thumb': "https://via.placeholder.com/400x225/111/333", 'qs': ["أفضل جودة"]}

# # 3. عرض اللوجو والعنوان الرئيسي
# st.markdown('<div class="logo-text">🌐 El_kasrawy </div>', unsafe_allow_html=True)
# st.markdown('<div class="glow-title">YouTube Downloader 🎬</div>', unsafe_allow_html=True)

# # 4. تقسيم الصفحة لعمودين (مكان الرابط + زر البحث)
# col_input, col_search = st.columns([4, 1])
# with col_input:
#     url_input = st.text_input("YouTube URL", placeholder="ضع رابط الفيديو هنا...", key="url_bar", label_visibility="collapsed")
# with col_search:
#     search_btn = st.button("🔍 بحث")

# # 5. منطق البحث: جلب معلومات الفيديو عند الضغط على زر البحث
# if search_btn and url_input:
#     try:
#         with st.spinner("🔄 جاري فحص الجودات بالهوية الجديدة..."):
#             # إعدادات مكتبة yt-dlp لجلب المعلومات باستخدام الكوكيز
#             ydl_opts = {
#                 'quiet': True, 
#                 'nocheckcertificate': True,
#                 'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
#                 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#             }
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url_input, download=False) # جلب المعلومات بدون تحميل
#                 formats = info.get('formats', [])
#                 # استخراج الجودات المتاحة (الطول) وترتيبها من الأعلى للأقل
#                 heights = sorted(list(set(f['height'] for f in formats if f.get('height'))), reverse=True)
#                 # تخزين البيانات في جلسة المستخدم
#                 st.session_state.video_data = {
#                     'title': info.get('title', 'Video'),
#                     'thumb': info.get('thumbnail'),
#                     'qs': [f"{h}p" for h in heights] if heights else ["أفضل جودة"]
#                 }
#     except Exception as e:
#         st.error(f"❌ خطأ: تأكد من رفع ملف cookies.txt | {e}")

# # 6. منطقة عرض تفاصيل الفيديو المختار وإعدادات التحميل
# main_col = st.container()
# with main_col:
#     st.markdown("### 📥 إعدادات التحميل")
#     col_m1, col_m2 = st.columns([1, 1.2])
#     with col_m1:
#         st.image(st.session_state.video_data['thumb'], width='stretch') # عرض صورة الفيديو
#     with col_m2:
#         st.write(f"**{st.session_state.video_data['title']}**") # عرض عنوان الفيديو
#         format_choice = st.selectbox("النوع:", ["فيديو (MP4)", "صوت (MP3)"]) # اختيار النوع
#         quality_choice = st.selectbox("الجودة:", st.session_state.video_data['qs']) # اختيار الجودة

#     # شريط التقدم ونصوص الحالة
#     progress_bar = st.progress(0)
#     status_text = st.empty()

#     # دالة لمتابعة تقدم التحميل وتحديث شريط التقدم برمجياً
#     def progress_hook(d):
#         if d['status'] == 'downloading':
#             p = d.get('_percent_str', '0%').replace('%','')
#             try:
#                 progress_bar.progress(float(p)/100)
#                 status_text.text(f"🚀 جاري التحميل: {d.get('_percent_str')}")
#             except: pass

#     # 7. منطق التحميل والمعالجة عند الضغط على زر "ابدأ المعالجة"
#     if st.button("🚀 ابدأ المعالجة"):
#         if url_input:
#             is_mp3 = "صوت" in format_choice
#             ext = "mp3" if is_mp3 else "mp4"
#             unique_id = uuid.uuid4().hex # توليد معرف فريد للملف لمنع التداخل
#             out_file = f"{unique_id}.{ext}" # اسم الملف النهائي
#             q_num = quality_choice.replace("p", "") # استخراج رقم الجودة فقط
            
#             # إعدادات التحميل النهائية
#             ydl_opts = {
#                 'format': f'bestvideo[height<={q_num}]+bestaudio/best' if not is_mp3 else 'bestaudio/best',
#                 'outtmpl': out_file, # مكان حفظ الملف
#                 'merge_output_format': 'mp4' if not is_mp3 else None,
#                 'progress_hooks': [progress_hook], # ربط دالة المتابعة
#                 'nocheckcertificate': True,
#                 'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
#                 'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#             }
#             # إذا كان الاختيار صوت، نقوم بإضافة معالج FFmpeg لتحويل الملف
#             if is_mp3:
#                 ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

#             try:
#                 with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                     ydl.download([url_input]) # بدء عملية التحميل الفعلية
                
#                 # التأكد من وجود الملف بعد التحميل ثم عرضه للمستخدم
#                 if os.path.exists(out_file):
#                     st.session_state.history.append({"title": st.session_state.video_data['title']}) # إضافة للسجل
#                     status_text.text("✅ تمت المعالجة! اضغط على الزر الأزرق")
#                     with open(out_file, "rb") as f:
#                         st.download_button(
#                             label="📥 حفظ الملف الآن",
#                             data=f,
#                             file_name=f"video_{unique_id}.{ext}",
#                             mime="video/mp4" if not is_mp3 else "audio/mpeg"
#                         )
#                 else: st.error("❌ فشل التحميل")
#             except Exception as e:
#                 st.error(f"❌ خطأ: {e}")

# # 8. القائمة الجانبية (Sidebar) لعرض سجل التحميلات
# with st.sidebar:
#     st.markdown("### 📜 السجل")
#     if st.button("🗑️ مسح السجل"):
#         st.session_state.history = []
#         st.rerun() # إعادة تحميل الصفحة لتصفير السجل
    
#     # عرض السجل بترتيب عكسي (الأحدث أولاً)
#     for item in reversed(st.session_state.history):
#         st.markdown(f'<div class="history-card"><b>{item["title"][:30]}</b></div>', unsafe_allow_html=True)

# # 9. التوقيع السفلي
# st.markdown("<br><center>El_kasrawy Pro 2025</center>", unsafe_allow_html=True)

# ================================================================================================================================

import streamlit as st
import yt_dlp
import os
import time
import uuid
import re
from config import apply_config

# تطبيق الإعدادات من ملف config
apply_config()

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
                'format': f'bestvideo[ext=mp4][height<={q_num}]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': out_file,
                'merge_output_format': 'mp4' if not is_mp3 else None,
                'ffmpeg_location': './ffmpeg.exe',
                'progress_hooks': [progress_hook],
                'nocheckcertificate': True,
                'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            if is_mp3:
                ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url_input])
                
                if os.path.exists(out_file):
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

with st.sidebar:
    st.markdown("### 📜 السجل")
    if st.button("🗑️ مسح السجل"):
        st.session_state.history = []
        st.rerun()
    
    for item in reversed(st.session_state.history):
        st.markdown(f'<div class="history-card"><b>{item["title"][:30]}</b></div>', unsafe_allow_html=True)

st.markdown("<br><center>El_kasrawy Pro 2025</center>", unsafe_allow_html=True)