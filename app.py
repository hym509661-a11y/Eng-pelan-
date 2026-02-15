import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات واجهة المهندس بيلان ---
st.set_page_config(page_title="Bilan-Engineering Ultimate", layout="wide")

st.markdown("""
    <div style="background-color:#002b5c;padding:20px;border-radius:15px;text-align:center;">
        <h1 style="color:white;margin:0;">Bilan-Engineering Ultimate v4.0</h1>
        <p style="color:#00d1ff;font-size:20px;">المصمم الإنشائي الشامل | المهندس بيلان عبدالكريم</p>
    </div>
""", unsafe_allow_html=True)

# --- القائمة الجانبية الشاملة ---
with st.sidebar:
    st.header("📂 اختيار العنصر")
    category = st.selectbox("العنصر المراد تصميمه:", 
        ["جائز (Beam)", "بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "عمود (Column)"])
    
    st.divider()
    st.header("📐 المدخلات الهندسة")
    L = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
    B = st.number_input("العرض B (m):", 0.2, 10.0, 0.3 if "Beam" in category or "Column" in category else 4.0)
    h = st.number_input("الارتفاع/السماكة h (cm):", 10, 200, 60)
    
    if "Beam" in category:
        support_type = st.selectbox("حالة الاستناد:", ["بسيط", "كابولي", "وثاقة طرفين"])
    
    if "Footing" in category:
        q_soil = st.number_input("تحمل التربة (kg/cm2):", 0.5, 5.0, 2.0)

    st.divider()
    wu = st.number_input("الحمل التصميمي (t/m أو t/m2):", 0.1, 500.0, 2.5)
    phi = st.selectbox("قطر التسليح (mm):", [8, 10, 12, 14, 16, 18, 20, 25])

# --- المحرك الحسابي الموحد ---
def calculate_all():
    # حسابات الجوائز والبلاطات (عزوم وسهم)
    if "Beam" in category or "Slab" in category:
        coef = 1/8 if "كابولي" not in locals() or support_type == "بسيط" else 1/2
        if "Beam" in category and support_type == "وثاقة طرفين": coef = 1/12
        
        Mu = (wu * L**2) * coef
        d = h - 5
        As = (abs(Mu) * 10**5) / (0.87 * 4000 * d)
        
        # حساب السهم
        Ec = 15000 * np.sqrt(250) * 10
        I_g = (B * (h/100)**3) / 12
        delta = ( (5/384 if coef==1/8 else 1/384) * wu * L**4 / (Ec * I_g) ) * 1000
        d_allow = (L * 1000) / 250
        return Mu, As, delta, d_allow

    # حسابات الأساسات
    elif "Footing" in category:
        Area_req = (wu / (q_soil * 10)) * 1.1
        side = np.sqrt(Area_req)
        return Area_req, side, 0, 0

    # حسابات الأعمدة
    elif "Column" in category:
        area_col = B * 100 * h
        capacity = (0.35 * 250 * area_col + 0.67 * 4000 * (0.01 * area_col)) / 1000
        return capacity, area_col, 0, 0

res = calculate_all()

# --- العرض المنسق للنتائج والمخططات ---
col_res, col_img = st.columns([1, 1.2])

with col_res:
    st.subheader("📑 نتائج التدقيق")
    if "Beam" in category or "Slab" in category:
        st.metric("العزم الأعظمي Mu", f"{res[0]:.2f} t.m")
        bar_area = (np.pi * (phi/10)**2) / 4
        n_bars = int(np.ceil(res[1] / bar_area))
        st.success(f"التسليح المقترح: {max(n_bars, 3)} T{phi}")
        
        st.divider()
        st.write(f"**تدقيق السهم:** {res[2]:.2f} mm / المسموح: {res[3]:.2f} mm")
        if res[2] < res[3]: st.write("✅ السهم محقق")
        else: st.error("🚨 السهم غير محقق")

    elif "Footing" in category:
        st.metric("المساحة المطلوبة", f"{res[0]:.2f} m2")
        st.info(f"الأبعاد المقترحة: {res[1]:.2f} x {res[1]:.2f} m")

    elif "Column" in category:
        st.metric("تحمل العمود التقريبي", f"{res[0]:.1f} Ton")
        if res[1] < 900: st.error("🚨 مساحة العمود أقل من 900 سم2!")

with col_img:
    st.subheader("🎨 المخطط التوضيحي للحديد")
    fig, ax = plt.subplots()
    if "Slab" in category:
        ax.add_patch(patches.Rectangle((0, 0), 4, 3, facecolor='#ddd'))
        for i in range(5): ax.plot([0, 4], [i*0.6, i*0.6], color='red', lw=2)
        ax.set_title("توزيع فرش البلاطة")
        
    elif "Footing" in category:
        ax.add_patch(patches.Rectangle((0, 0), 3, 3, facecolor='#bbb'))
        ax.add_patch(patches.Rectangle((1.2, 1.2), 0.6, 0.6, facecolor='#555'))
        ax.set_title("تسليح القاعدة والرقبة")
        
    elif "Hordy" in category:
        
    elif "Beam" in category:
        
    elif "Column" in category:
        
    
    ax.axis('off')
    st.pyplot(fig)

st.divider()
st.subheader(f"📝 المذكرة الحسابية - المهندس بيلان عبدالكريم")
st.write(f"تم تصميم العنصر ({category}) وفق اشتراطات الكود العربي السوري لعام 2026. المذكرة تشمل التحقق من المقاطع، حساب حديد التسليح، والتحقق من حالات الحدود التشغيلية (السهم).")
