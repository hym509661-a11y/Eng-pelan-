import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import ezdxf  # مكتبة الأوتوكاد الاحترافية

# الهوية المهنية
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"

# دالة لتصحيح النصوص العربية في الرسم (حل مشكلة الحروف المقلوبة)
def fix_arabic(text):
    return text[::-1] # حل مؤقت وسريع لعرض الحروف في Matplotlib

st.set_page_config(page_title="Pelan Office v121", layout="wide")

st.title(f"🏛️ نظام {ST_NAME} - الإصدار v121")

# --- مدخلات التصميم ---
with st.sidebar:
    st.header("⚙️ إعدادات المقطع")
    b = st.number_input("العرض B (cm)", 20, 100, 30)
    h = st.number_input("الارتفاع H (cm)", 20, 200, 60)
    nb = st.number_input("عدد القضبان السفلي", 2, 12, 4)
    db = st.selectbox("قطر السفلي", [14, 16, 18, 20], index=1)
    nt = st.number_input("عدد القضبان العلوي", 2, 12, 2)
    dt = st.selectbox("قطر العلوي", [10, 12, 14, 16], index=1)

# --- الرسم داخل التطبيق (بخطوط صحيحة) ---
fig, ax = plt.subplots(figsize=(5, 7))
ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=3))
ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1.5, ls='--'))

# حديد سفلي وعلوي
x_bot = np.linspace(6, b-6, nb); ax.scatter(x_bot, [6]*nb, color='blue', s=120)
x_top = np.linspace(6, b-6, nt); ax.scatter(x_top, [h-6]*nt, color='darkred', s=100)

# كتابة التسميات (تم تعديلها لتظهر بوضوح)
ax.text(b/2, -10, f"MAIN: {nb} T {db}", color='blue', ha='center', weight='bold', fontsize=12)
ax.text(b/2, h+5, f"TOP: {nt} T {dt}", color='darkred', ha='center', weight='bold', fontsize=12)
ax.set_title(fix_arabic("المقطع الإنشائي المعتمد"), fontsize=15) # تصحيح العنوان

plt.axis('off')
st.pyplot(fig)

st.divider()

# --- قسم التصدير (الحل النهائي للأوتوكاد) ---
st.subheader("📥 تصدير المخططات والحسابات")

col1, col2 = st.columns(2)

with col1:
    # إنشاء ملف DXF حقيقي باستخدام ezdxf
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # رسم برواز الخرسانة في أوتوكاد
    msp.add_lwpolyline([(0, 0), (b, 0), (b, h), (0, h), (0, 0)])
    # إضافة نص داخل أوتوكاد
    msp.add_text(f"BEAM {b}x{h}", dxfattribs={'height': 5}).set_placement((5, h+5))
    
    # حفظ الملف في ذاكرة مؤقتة
    dxf_stream = io.StringIO()
    doc.write(dxf_stream)
    
    st.download_button(
        label="🚀 تحميل مخطط AutoCAD (ملف DXF حقيقي)",
        data=dxf_stream.getvalue(),
        file_name=f"Pelan_Drawing.dxf",
        mime="application/dxf"
    )

with col2:
    # تصدير الإكسل
    output = io.BytesIO()
    df = pd.DataFrame({"العنصر": ["جائز"], "التسليح": [f"{nb}T{db} + {nt}T{dt}"]})
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="📊 تحميل المذكرة الحسابية (Excel)",
        data=output.getvalue(),
        file_name="Pelan_Report.xlsx",
        mime="application/vnd.ms-excel"
    )

# الختم الجانبي الثابت
st.sidebar.markdown(f"""
<div style="border:2px solid #d4af37; padding:10px; text-align:center; background:white; color:black; border-radius:10px; margin-top:20px;">
    <p>المهندس المدني</p>
    <p style="color:#d4af37; font-size:18px;"><b>{ST_NAME}</b></p>
    <p>TEL: {ST_TEL}</p>
</div>
""", unsafe_allow_html=True)
