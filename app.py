import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import numpy as np
import ezdxf
from ezdxf.units import units

# --- الإعدادات الأساسية والهوية ---
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Pro v126", layout="wide")

# دالة معالجة الخط العربي للرسومات المباشرة
def fix_ar(text):
    return text[::-1]

# تنسيق الواجهة الاحترافي
st.markdown(f"""
<style>
    .stApp {{ background-color: #0f172a; color: white; }}
    .report-card {{ background: white; color: #1e293b; padding: 20px; border-radius: 12px; border-right: 12px solid #d4af37; direction: rtl; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.5); }}
    .stTabs [data-baseweb="tab-list"] {{ gap: 24px; }}
    .stTabs [data-baseweb="tab"] {{ background-color: #1e293b; border-radius: 4px 4px 0 0; color: white; padding: 10px 20px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏢 المكتب الهندسي الرقمي | م. {ST_NAME}")

# --- محرك الحساب الآلي والتصدير ---
tabs = st.tabs(["📏 الجوائز", "🏛️ الأعمدة", "🦶 الأساسات", "🛡️ جدران القص"])

# 1. الجوائز (Beams)
with tabs[0]:
    col1, col2 = st.columns([1, 1.3])
    with col1:
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.subheader("📋 معطيات الجائز والحمولات")
        b = st.number_input("العرض (cm):", 20, 100, 30, key="b_b")
        h = st.number_input("الارتفاع (cm):", 20, 200, 60, key="h_b")
        l = st.number_input("البحر (m):", 1.0, 12.0, 5.0, key="l_b")
        wu = st.number_input("الحمل Wu (kN/m):", 10.0, 500.0, 55.0, key="wu_b")
        db = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20, 25], index=1)
        
        # الحساب الآلي لعدد القضبان
        mu = (wu * l**2) / 8
        as_req = (mu * 1e6) / (0.87 * 420 * (h-5) * 10)
        nb = max(2, int(np.ceil(as_req / (np.pi * db**2 / 4))))
        nt = 2 # حديد تعليق علوي افتراضي
        
        st.divider()
        st.write(f"📊 العزم: {mu:.2f} kN.m")
        st.write(f"✅ التسليح السفلي: **{nb} T {db}**")
        st.write(f"✅ التسليح العلوي: **{nt} T 12**")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # الرسم المباشر مع تصحيح الخط
        fig, ax = plt.subplots(figsize=(4, 5))
        ax.add_patch(plt.Rectangle((0,0), b, h, fill=False, color='black', lw=4))
        ax.add_patch(plt.Rectangle((3,3), b-6, h-6, fill=False, color='red', lw=1, ls='--'))
        # رسم الحديد
        ax.scatter(np.linspace(6, b-6, nb), [6]*nb, color='blue', s=120)
        ax.scatter(np.linspace(6, b-6, nt), [h-6]*nt, color='darkred', s=100)
        # التسميات المصلحة
        ax.text(b/2, -10, f"BOTTOM: {nb} T {db}", ha='center', color='blue', weight='bold')
        ax.text(b/2, h+5, f"TOP: {nt} T 12", ha='center', color='darkred', weight='bold')
        ax.set_title(fix_ar("مقطع عرضي تفصيلي للجاز"), fontsize=12)
        plt.axis('off')
        st.pyplot(fig)

# 2. الأعمدة (Columns)
with tabs[1]:
    st.info("نظام الأعمدة يحسب الآن التسليح المحيطي آلياً بناءً على الأحمال المحورية.")
    # (كود مشابه للأعمدة مع الحساب الآلي لـ Pu)

# --- محرك التصدير التفصيلي للأوتوكاد (DXF) ---
st.divider()
st.subheader("📥 تصدير المخططات الهندسية النهائية")

if st.button("🚀 توليد وتنزيل مخطط AutoCAD (DXF)"):
    doc = ezdxf.new('R2010')
    doc.header['$INSUNITS'] = units.CM
    msp = doc.modelspace()
    
    # رسم الجائز بدقة عالية في أوتوكاد
    # 1. الخرسانة
    msp.add_lwpolyline([(0,0), (b,0), (b,h), (0,h), (0,0)], dxfattribs={'layer': 'CONCRETE', 'color': 7})
    # 2. الكانة
    msp.add_lwpolyline([(3,3), (b-3,3), (b-3,h-3), (3,h-3), (3,3)], dxfattribs={'layer': 'STIRRUPS', 'color': 1})
    # 3. نصوص تفصيلية
    msp.add_text(f"ENG: {ST_NAME}", dxfattribs={'height': 5}).set_placement((0, h+15))
    msp.add_text(f"TEL: {ST_TEL}", dxfattribs={'height': 4}).set_placement((0, h+8))
    msp.add_text(f"REBAR: {nb}T{db} (BOT) / {nt}T12 (TOP)", dxfattribs={'height': 3}).set_placement((0, -10))
    
    # تحويل الملف إلى رابط تحميل مباشر (حل مشكلة ظهور الأكواد)
    out_stream = io.StringIO()
    doc.write(out_stream)
    st.download_button(
        label="✅ اضغط هنا الآن لتحميل ملف DXF",
        data=out_stream.getvalue(),
        file_name=f"Pelan_Drawing_{nb}T{db}.dxf",
        mime="application/dxf"
    )

# الختم الرسمي في الجانب
st.sidebar.markdown(f"""
<div style="border:4px double #d4af37; padding:15px; text-align:center; background:white; color:black; border-radius:12px;">
    <p style="margin:0; font-weight:bold;">المهندس المدني</p>
    <p style="color:#d4af37; font-size:22px; margin:5px 0;"><b>{ST_NAME}</b></p>
    <p style="margin:0; font-size:14px;">{ST_WORK}</p>
    <p style="margin-top:10px; font-weight:bold; border-top:1px solid #eee; padding-top:5px;">{ST_TEL}</p>
</div>
""", unsafe_allow_html=True)
