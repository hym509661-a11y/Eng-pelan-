import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import base64

# الهوية المهنية المعتمدة
ST_NAME, ST_TEL = "بيلان مصطفى عبد الكريم", "0998449697"

st.set_page_config(page_title="Pelan Office v120", layout="wide")

# دالة الرسم المحدثة (علوي + سفلي + تسميات)
def draw_professional_section(b, h, n_bot, d_bot, n_top, d_top, title):
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=3))
    ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1.5, ls='--'))
    
    # رسم وتسمية السفلي
    x_bot = np.linspace(6, b-6, n_bot) if n_bot > 1 else [b/2]
    ax.scatter(x_bot, [6]*len(x_bot), color='blue', s=100)
    ax.text(b/2, -10, f"MAIN: {n_bot} T {d_bot}", color='blue', ha='center', weight='bold')
    
    # رسم وتسمية العلوي
    x_top = np.linspace(6, b-6, n_top) if n_top > 1 else [b/2]
    ax.scatter(x_top, [h-6]*len(x_top), color='darkred', s=80)
    ax.text(b/2, h+5, f"TOP: {n_top} T {d_top}", color='darkred', ha='center', weight='bold')
    
    ax.set_title(title, pad=20)
    ax.set_aspect('equal')
    plt.axis('off')
    return fig

# واجهة المستخدم
st.title(f"🏛️ نظام {ST_NAME} - v120")

with st.expander("🛠️ إعدادات التصميم والتسليح", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        b = st.number_input("العرض B (cm)", 20, 100, 30)
        h = st.number_input("الارتفاع H (cm)", 20, 200, 60)
    with col2:
        nb = st.number_input("عدد السفلي", 2, 12, 4)
        db = st.selectbox("قطر السفلي", [14, 16, 18, 20], index=1)
    with col3:
        nt = st.number_input("عدد العلوي", 2, 12, 2)
        dt = st.selectbox("قطر العلوي", [10, 12, 14, 16], index=1)

st.pyplot(draw_professional_section(b, h, nb, db, nt, dt, "المقطع الإنشائي المعتمد"))

st.divider()

# --- الحل النهائي لمشكلة الأوتوكاد (DXF) ---
def get_dxf_download_link(b, h, nb, db, nt, dt):
    # بناء ملف DXF متوافق برمجياً
    dxf_data = f"""0
SECTION
2
HEADER
9
$ACADVER
1
AC1027
0
ENDSEC
0
SECTION
2
ENTITIES
0
LINE
8
Concrete
10
0.0
20
0.0
11
{b}
21
0.0
0
LINE
8
Concrete
10
{b}
20
0.0
11
{b}
21
{h}
0
LINE
8
Concrete
10
{b}
20
{h}
11
0.0
21
{h}
0
LINE
8
Concrete
10
0.0
20
{h}
11
0.0
21
0.0
0
ENDSEC
0
EOF"""
    b64 = base64.b64encode(dxf_data.encode()).decode()
    return f'<a href="data:application/dxf;base64,{b64}" download="Pelan_Detail.dxf" style="text-decoration:none;"><button style="background-color:#d4af37; color:white; padding:15px; border-radius:10px; border:none; width:100%; cursor:pointer; font-weight:bold;">🚀 تحميل ملف AutoCAD المطور (DXF)</button></a>'

st.markdown(get_dxf_download_link(b, h, nb, db, nt, dt), unsafe_allow_html=True)

# الختم
st.sidebar.markdown(f"""
<div style="border:3px double #d4af37; padding:10px; text-align:center; background:white; color:black; border-radius:10px;">
    <p>المهندس المدني</p>
    <p style="color:#d4af37; font-size:20px;"><b>{ST_NAME}</b></p>
    <p>TEL: {ST_TEL}</p>
</div>
""", unsafe_allow_html=True)
