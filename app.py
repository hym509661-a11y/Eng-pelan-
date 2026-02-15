import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات واجهة المهندس بيلان
st.set_page_config(page_title="Bilan-Engineering Suite", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Pro v2.0</h1>
        <p style="color:#00d1ff;font-size:20px;">تصميم: المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# قائمة الاختيارات
with st.sidebar:
    st.header("🛠️ لوحة التحكم")
    category = st.selectbox("العنصر الإنشائي:", 
        ["بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "جائز (Beam)", "عمود (Column)"])
    
    st.divider()
    L = st.number_input("الطول أو البحر L (m):", 1.0, 20.0, 5.0)
    B = st.number_input("العرض B (m):", 0.2, 10.0, 0.3)
    t = st.number_input("السماكة t (cm):", 10, 100, 25)
    
    st.divider()
    phi = st.selectbox("قطر السيخ المستخدم (mm):", [8, 10, 12, 14, 16, 20, 25])
    fy = 4000

# المحرك الحسابي
def solve_design():
    # حسابات افتراضية للأحمال
    wu = 1.2 # t/m2
    Mu = (wu * L**2) / 8
    d = t - 3 # cover
    As_req = (Mu * 10**5) / (0.87 * fy * d)
    
    # حساب عدد الأسياخ
    bar_area = (np.pi * (phi/10)**2) / 4
    n_bars = int(np.ceil(As_req / bar_area))
    if n_bars < 3: n_bars = 3
    
    return Mu, As_req, n_bars

Mu, As, bars = solve_design()

# العرض والنتائج
col1, col2 = st.columns([1.5, 1])

with col1:
    st.subheader(f"📊 المخطط الإنشائي لـ {category}")
    fig, ax = plt.subplots(figsize=(10, 5))
    
    if "Slab" in category:
        # رسم البلاطة والفرش
        ax.add_patch(patches.Rectangle((0, 0), L, B, facecolor='#e0e0e0', edgecolor='black'))
        for i in range(10): # تمثيل الحديد
            ax.plot([0, L], [i*B/10, i*B/10], color='red', lw=1, alpha=0.6)
        ax.set_title("مخطط توزيع فرش التسليح (Bottom Rebars)")
        
    elif "Footing" in category:
        # رسم القاعدة
        ax.add_patch(patches.Rectangle((0, 0), 2, 2, facecolor='#b0b0b0', edgecolor='black'))
        ax.add_patch(patches.Rectangle((0.85, 0.85), 0.3, 0.3, facecolor='#606060'))
        ax.set_title("مسقط أفقي للقاعدة المنفردة وتوزع الأساور")
        
    elif "Beam" in category:
        ax.add_patch(patches.Rectangle((0, 0.4), L, 0.2, facecolor='#cccccc'))
        ax.plot([0, L], [0.42, 0.42], color='blue', lw=3) # الحديد السفلي
        ax.set_title("تفريد حديد الجائز (Beam Detailing)")
        
    ax.axis('off')
    st.pyplot(fig)

with col2:
    st.subheader("📝 تقرير المهندس بيلان")
    st.info(f"العزم التصميمي: {Mu:.2f} t.m")
    st.success(f"التسليح المحسوب: {bars} T{phi}")
    
    st.divider()
    st.write("### المذكرة الحسابية")
    st.latex(r"A_s = \frac{M_u}{0.87 \cdot f_y \cdot d}")
    st.write(f"المساحة المطلوبة: {As:.2f} cm²")
    st.write(f"المساحة المحققة: {bars * ((np.pi*(phi/10)**2)/4):.2f} cm²")
    
    if "Column" in category and (B*100*t) < 900:
        st.error("🚨 إنذار الكود السوري: مساحة العمود أقل من 900 سم²")

st.divider()
st.subheader("🧱 تفاصيل إنشائية توضيحية")
if "Hordy" in category:
        st.write("تفصيل توزيع البلوك والحديد في البلاطة الهوردي.")
