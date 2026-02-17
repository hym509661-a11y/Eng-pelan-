import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import ezdxf  # مكتبة لإنشاء ملفات الأوتوكاد

# إعدادات الواجهة
st.set_page_config(page_title="Ultimate Engineering Suite", layout="wide")
st.title("🏗️ النظام الهندسي المتكامل (Analysis, Design & CAD)")

# --- 1. مدخلات النمذجة (ETABS Style) ---
st.sidebar.header("1. النمذجة الإنشائية")
nodes = st.sidebar.number_input("عدد العقد (Nodes)", min_value=2, value=2)
loads = st.sidebar.number_input("الحمل الحي (kN/m2)", value=5.0)
f_c = st.sidebar.slider("f'c (MPa)", 20, 60, 30)
f_y = st.sidebar.slider("fy (MPa)", 240, 420, 400)

# --- 2. محرك التحليل الإنشائي (Structural Solver) ---
st.header("📊 مخرجات التحليل الإنشائي (ETABS Engine)")
# افتراض كمرة بسيطة لتحليل العزوم والقوى
L = 6.0 # طول افتراضي
x = np.linspace(0, L, 100)
moment = (loads * x / 2) * (L - x) # M = wL/2 * x - wx^2/2

fig, ax = plt.subplots()
ax.plot(x, moment, label="Bending Moment (kNm)", color='red')
ax.fill_between(x, moment, color='red', alpha=0.2)
ax.set_title("Bending Moment Diagram (BMD)")
st.pyplot(fig)


# --- 3. تصميم العناصر الإنشائية (SAFE Style) ---
st.header("🏗️ تصميم المقاطع (SAFE/Concrete Design)")
b = 300; d = 500 # أبعاد افتراضية بالـ mm
Mu = np.max(moment) * 10**6 # تحويل لـ N.mm
# حساب التسليح (تبسيط كود ACI)
Rn = Mu / (0.9 * b * d**2)
rho = (0.85 * f_c / f_y) * (1 - np.sqrt(1 - (2 * Rn / (0.85 * f_c))))
As = rho * b * d
st.success(f"مساحة التسليح المطلوبة: {As:.2f} mm²")

# --- 4. توليد المخططات الهندسية (AutoCAD Style) ---
st.header("🖋️ تصدير المخططات (AutoCAD Export)")
def create_dxf():
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()
    # رسم مستطيل يمثل الكمرة
    msp.add_lwpolyline([(0, 0), (L*100, 0), (L*100, d/10), (0, d/10), (0, 0)], close=True)
    # رسم خطوط التسليح
    msp.add_line((5, 5), (L*100-5, 5), dxfattribs={'color': 1}) # تسليح سفلي
    doc.saveas("structural_detail.dxf")

if st.button("توليد ملف DXF للأوتوكاد"):
    create_dxf()
    with open("structural_detail.dxf", "rb") as file:
        st.download_button("تحميل المخطط الهندسي", file, "beam_detail.dxf")

# التذييل المطلوب
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
