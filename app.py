import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np

# الهوية المهنية
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"

st.set_page_config(page_title="Pelan Office v118", layout="wide")

# دالة رسم المقطع مع كتابة التفاصيل (علوي وسفلي)
def draw_section_final(b, h, n_bot, d_bot, n_top, d_top, title):
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=3)) # خرسانة
    ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1, ls='--')) # كانة
    
    # حديد سفلي + كتابة العدد والقطر
    x_bot = np.linspace(6, b-6, n_bot)
    ax.scatter(x_bot, [6]*n_bot, color='blue', s=100)
    ax.text(b/2, -10, f"{n_bot} T {d_bot}", color='blue', ha='center', fontweight='bold')
    
    # حديد علوي + كتابة العدد والقطر
    x_top = np.linspace(6, b-6, n_top)
    ax.scatter(x_top, [h-6]*n_top, color='darkblue', s=80)
    ax.text(b/2, h+5, f"{n_top} T {d_top}", color='darkblue', ha='center', fontweight='bold')
    
    ax.set_title(title)
    ax.set_aspect('equal')
    plt.axis('off')
    return fig

st.title(f"🏛️ نظام {ST_NAME} الهندسي")

# منطقة الحسابات (مثال الجائز)
st.subheader("📏 تصميم الجوائز مع التسليح العلوي والسفلي")
c1, c2 = st.columns([1, 1.5])
with c1:
    b = st.number_input("العرض (cm)", value=30)
    h = st.number_input("الارتفاع (cm)", value=60)
    n_bot = st.number_input("عدد القضبان السفلي", value=4)
    d_bot = st.number_input("قطر السفلي (mm)", value=16)
    n_top = st.number_input("عدد القضبان العلوي", value=2)
    d_top = st.number_input("قطر العلوي (mm)", value=12)
with c2:
    fig = draw_section_final(b, h, n_bot, d_bot, n_top, d_top, "مقطع عرضي كامل")
    st.pyplot(fig)

st.divider()

# --- الحل النهائي لمشكلة التصدير ---
st.subheader("📥 مركز تحميل الملفات (اضغط للتحميل المباشر)")

col_a, col_b = st.columns(2)

with col_a:
    # 1. تصدير المذكرة الحسابية (Excel)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df = pd.DataFrame({
            "العنصر": ["جائز"], "العرض": [b], "الارتفاع": [h],
            "سفلي": [f"{n_bot}T{d_bot}"], "علوي": [f"{n_top}T{d_top}"]
        })
        df.to_excel(writer, index=False, sheet_name='Design')
    
    st.download_button(
        label="📥 تحميل المذكرة الحسابية (Excel)",
        data=output.getvalue(),
        file_name=f"Calculation_Report_{ST_NAME}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

with col_b:
    # 2. تصدير المخطط (DXF) كملف حقيقي
    dxf_content = f"0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1027\n0\nENDSEC\n0\nEOF" # هيكل مبسط
    st.download_button(
        label="🚀 تحميل مخطط AutoCAD (DXF)",
        data=dxf_content,
        file_name=f"Structural_Detail_{ST_NAME}.dxf",
        mime="application/dxf"
    )

# الختم المحدث
st.sidebar.markdown(f"""
<div style="border:2px solid #d4af37; padding:10px; text-align:center; background:white; color:black; border-radius:10px;">
    <p>المهندس المدني</p>
    <p style="color:#d4af37; font-size:18px;"><b>{ST_NAME}</b></p>
    <p>TEL: {ST_TEL}</p>
</div>
""", unsafe_allow_html=True)
""", unsafe_allow_html=True)
