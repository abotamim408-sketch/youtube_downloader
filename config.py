# import streamlit as st

# # دالة لإعداد تنسيقات الصفحة والـ CSS
# def apply_custom_styles():
#     # ضبط إعدادات الصفحة مثل العنوان وتخطيط العرض الواسع
#     st.set_page_config(page_title="YouTube Downloader", layout="wide")

#     # كود CSS لتغيير شكل التطبيق (الألوان، الخلفية، الأزرار)
#     st.markdown("""
#         <style>
#         /* تغيير خلفية التطبيق للون الداكن */
#         .stApp { background-color: #0b0e14; color: white; }
#         /* تنسيق نص اللوجو العلوي */
#         .logo-text { color: #00c6ff; font-size: 22px; font-weight: bold; }
#         /* تنسيق العنوان الرئيسي المتوهج */
#         .glow-title { font-size: 40px; font-weight: 900; color: #FFFFFF; text-align: center; }
        
#         /* تنسيق أزرار البحث والمعالجة (شفافة بحدود زرقاء) */
#         div.stButton > button {
#             background-color: transparent; color: #00c6ff; border: 2px solid #00c6ff;
#             border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
#         }
#         /* تغيير لون الزرار عند مرور الماوس عليه */
#         div.stButton > button:hover { background-color: #00c6ff; color: white; }
        
#         /* تنسيق زر التحميل النهائي (لون أزرق كامل) */
#         div.stDownloadButton > button {
#             background-color: #00c6ff !important; 
#             color: white !important; 
#             border: none !important;
#             border-radius: 10px; font-weight: bold; width: 100%; height: 3.5em;
#             font-size: 18px;
#         }
        
#         /* تنسيق كروت السجل (History) في القائمة الجانبية */
#         .history-card { background: rgba(255,255,255,0.05); padding: 10px; border-radius: 10px; margin-bottom: 5px; border-right: 4px solid #00c6ff; }
#         </style>
#         """, unsafe_allow_html=True)

# ==================================================================================================================================================================

import streamlit as st

def apply_config():
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