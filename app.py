import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF

# إعدادات الواجهة
st.set_page_config(page_title="المصمم الإنشائي - نسخة المحترفين", layout="wide")
st.title("🏗️ نظام التصميم والتحليل الإنشائي (Interaction Diagram)")

# --- دالة رسم مخطط التفاعل (Interaction Diagram) ---
def plot_interaction(b, h, fcu, fy, num_bars, bar_dia):
    As_total = num_bars * (math.pi * bar_dia**2 / 4)
    Ag = b * h * 100
    # نقاط مبسطة لرسم منحنى التفاعل
    P0 = (0.35 * fcu * (Ag - As_total) + 0.67 * fy * As_total) / 10000 # Ton
    Pb = 0.3 * P0 # نقطة التوازن التقريبية
    Mb = (Pb * h / 5) # عزم التوازن التقريبي
    
    # توليد المنحنى
    p_points = [P0, P0*0.9, Pb, 0]
    m_points = [0, Mb*0.2, Mb, 0]
    
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.plot(m_points, p_points, 'b-', lw=2, label='Interaction Curve')
    ax.fill_between(m_points, p_points, color='blue', alpha=0.1)
    ax.set_xlabel("Moment Mu (t.m)")
    ax.set_ylabel("Axial Load Pu (Ton)")
    ax.grid(True, linestyle='--')
    return fig

# --- القائمة الرئيسية ---
with st.sidebar:
    st.header("⚙️ معطيات المواد")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

menu = ["تصميم الأعمدة الشامل", "تصميم البلاطات والأساسات"]
choice = st.selectbox("🎯 اختر المهمة:", menu)

if choice == "تصميم الأعمدة الشامل":
    st.header("🏢 تصميم الأعمدة مع مخطط التفاعل")
    c1, c2 = st.columns(2)
    with c1:
        P_u = st.number_input("الحمل Pu (Ton)", value=120.0)
        M_u = st.number_input("العزم Mu (t.m)", value=15.0)
    with c2:
        b = st.number_input("العرض b (cm)", value=30)
        h = st.number_input("العمق h (cm)", value=50)
        bar_dia = st.selectbox("قطر السيخ (mm)", [14, 16, 18, 20, 25])

    if st.button("تحليل المقطع ورسم المخطط"):
        # حسابات التسليح
        Ag = b * h * 100
        As_min = 0.008 * Ag
        # تقدير مبدئي لعدد القضبان بناءً على الأحمال
        As_req = (P_u*10000 - 0.35*fcu*Ag) / (0.67*fy - 0.35*fcu)
        As_final = max(As_req, As_min)
        num_bars = math.ceil(As_final / (math.pi * bar_dia**2 / 4))
        if num_bars % 2 != 0: num_bars += 1
        
        # النتائج والرسوم
        st.divider()
        res1, res2 = st.columns(2)
        
        with res1:
            st.subheader("🎨 مقطع العمود")
            fig_sect, ax_s = plt.subplots(figsize=(4, 4))
            ax_s.add_patch(plt.Rectangle((0, 0), b, h, color='lightgray'))
            # رسم الكانات والحديد
            ax_s.plot([2, b-2, b-2, 2, 2], [2, 2, h-2, h-2, 2], 'k-')
            for i in range(num_bars): # توزيع بسيط للرسم
                ax_s.plot(b/2, h/2, 'ro') # تمثيل للحديد
            st.pyplot(fig_sect)
            

        with res2:
            st.subheader("📉 مخطط التفاعل")
            fig_int = plot_interaction(b, h, fcu, fy, num_bars, bar_dia)
            # إضافة النقطة التصميمية
            plt.plot(M_u, P_u, 'ro', label='Design Point')
            plt.legend()
            st.pyplot(fig_int)
            

        # التقرير
        st.success(f"✅ تم التصميم: استخدم {num_bars} T{bar_dia}")
        report_txt = f"Report:\nPu={P_u}T, Mu={M_u}T.m\nSection: {b}x{h}cm\nSteel: {num_bars}T{bar_dia}"
        st.download_button("📥 تحميل التقرير PDF", report_txt, "Report.txt") # يمكن تحويله لـ PDF كما فعلنا سابقاً
