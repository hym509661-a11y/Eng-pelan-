import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# إعدادات الهوية البصرية للبرنامج
st.set_page_config(page_title="برنامج المهندس بيلان الإنشائي", layout="wide")

# الختم الخاص بك (يظهر في كل التقارير)
STAMP = """
المهندس المدني بيلان مصطفى عبدالكريم
دراسات - اشراف - تعهدات | 0998449697
"""

def draw_section(b, h, bars_count, bar_dia):
    """رسم مقطع عرضي في العنصر مع تفريد الحديد"""
    fig, ax = plt.subplots(figsize=(4, 4))
    # رسم الخرسانة
    rect = plt.Rectangle((0, 0), b, h, color='lightgrey', label='Concrete')
    ax.add_patch(rect)
    # رسم الحديد (مثال مبسط)
    cover = 2.5
    spacing = (b - 2*cover) / (bars_count - 1) if bars_count > 1 else 0
    for i in range(bars_count):
        circle = plt.Circle((cover + i*spacing, cover), bar_dia/10, color='red')
        ax.add_patch(circle)
        circle2 = plt.Circle((cover + i*spacing, h-cover), bar_dia/10, color='red')
        ax.add_patch(circle2)
    
    ax.set_xlim(-5, b+5)
    ax.set_ylim(-5, h+5)
    ax.set_aspect('equal')
    plt.title(f"مقطع عرضي {b}x{h}")
    return fig

# القائمة الجانبية لاختيار العنصر (مثل تبويبات الجواد)
st.sidebar.title("🏗️ قائمة العناصر")
choice = st.sidebar.radio("اختر نوع الدراسة:", 
    ["الجوائز المستمرة (عزوم وقص)", "الأعمدة والتحميل الشاقولي", "الأساسات (فرش وغطاء)", "البلاطات المسمطة"])

st.title(f"تحليل وتصميم: {choice}")

# منطقة المدخلات المشتركة
with st.expander("المعطيات العامة (الكود العربي السوري)"):
    col_m1, col_m2 = st.columns(2)
    fcu = col_m1.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = col_m2.number_input("إجهاد الشد fy (MPa)", value=400)

if choice == "الجوائز المستمرة (عزوم وقص)":
    L = st.number_input("طول المجاز (m)", value=5.0)
    w = st.number_input("الحمولة الموزعة (kN/m)", value=30.0)
    
    # حسابات العزوم والقص (بسيطة كمثال)
    M_max = (w * L**2) / 8
    V_max = (w * L) / 2
    
    st.info(f"العزم الأعظمي: {M_max:.2f} kN.m | القص الأعظمي: {V_max:.2f} kN")
    
    # رسم مخطط العزوم
    x = np.linspace(0, L, 100)
    y = (w * x / 2) * (L - x)
    fig_m, ax_m = plt.subplots()
    ax_m.plot(x, y, label="Moment Diagram")
    ax_m.invert_yaxis() # العزم لأسفل في البيتون
    st.pyplot(fig_m)

elif choice == "الأساسات (فرش وغطاء)":
    P = st.number_input("الحمولة المنقولة من العمود (kN)", value=1200)
    sigma_allow = st.number_input("إجهاد التربة المسموح (kg/cm2)", value=2.0)
    
    area_req = (P / 100) / sigma_allow # تحويل تقريبي
    side = np.sqrt(area_req)
    
    st.success(f"الأبعاد المقترحة للأساس: {side:.2f} m x {side:.2f} m")
    st.write("تفريد الحديد (فرش وغطاء): يتم حساب القطر بناءً على العزم عند وجه العمود.")

# منطقة المخرجات النهائية والختم
st.markdown("---")
if st.button("إصدار تقرير التصميم النهائي"):
    st.subheader("التقرير الفني النهائي")
    st.write(f"تم التصميم وفق معطيات المشروع المقدمة.")
    st.pyplot(draw_section(30, 60, 4, 16)) # رسم افتراضي للمقطع
    st.code(STAMP, language="") # عرض الختم بشكل رسمي
