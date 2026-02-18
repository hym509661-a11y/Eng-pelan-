import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# 1. إعدادات الواجهة المتطورة
st.set_page_config(page_title="Pelan Structural Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .header-box {
        background: linear-gradient(90deg, #1e293b, #334155);
        padding: 20px; border-radius: 15px; border: 1px solid #38bdf8;
        text-align: center; margin-bottom: 25px;
    }
    .support-box {
        background-color: #1e293b; padding: 15px; border-radius: 10px;
        border: 1px solid #94a3b8; text-align: center;
    }
    </style>
    <div class="header-box">
        <h1 style='color: #38bdf8; margin:0;'>Pelan Structural Analysis Pro</h1>
        <p style='color: #94a3b8;'>نظام التحليل الإنشائي المتطور | م. بيلان عبد الكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. القائمة الجانبية للمدخلات الهندسية
with st.sidebar:
    st.header("⚙️ الإعدادات العامة")
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 6.0)
    wu = st.number_input("الحمل الموزع Wu (t/m):", 0.1, 50.0, 3.0)
    
    st.divider()
    st.subheader("🧪 خصائص المقطع")
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 10, 200, 60)
    phi = st.selectbox("قطر التسليح (mm):", [12, 14, 16, 18, 20, 25])
    fy = 4000

# 3. اختيار المساند التفاعلي (Interactive Support Selection)
st.subheader("📍 نمذجة المساند (Support Modeling)")
col_s1, col_gap, col_s2 = st.columns([1, 0.5, 1])

with col_s1:
    st.markdown("<div class='support-box'><b>المسند الأيسر (Left)</b></div>", unsafe_allow_html=True)
    left_sup = st.radio("نوع المسند (A):", ["وثاقة (Fixed)", "مفصلي (Hinged)"], key="left")
    if left_sup == "وثاقة (Fixed)":
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Fixed_support.svg", width=80)
    else:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hinged_support.svg/200px-Hinged_support.svg.png", width=80)

with col_s2:
    st.markdown("<div class='support-box'><b>المسند الأيمن (Right)</b></div>", unsafe_allow_html=True)
    right_sup = st.radio("نوع المسند (B):", ["وثاقة (Fixed)", "مفصلي (Hinged)", "كابولي (Free)"], key="right")
    if right_sup == "وثاقة (Fixed)":
        st.image("https://upload.wikimedia.org/wikipedia/commons/4/47/Fixed_support.svg", width=80)
    elif right_sup == "مفصلي (Hinged)":
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Hinged_support.svg/200px-Hinged_support.svg.png", width=80)
    else:
        st.image("https://cdn-icons-png.flaticon.com/512/107/107794.png", width=60) # رمز تقريبي للكابولي

# 4. محرك التحليل الإنشائي (Structural Engine)
x = np.linspace(0, L, 500)
# دالة لحساب العزم والقص بناء على نوع الجملة
def analyze():
    # وثاقة - وثاقة
    if left_sup == "وثاقة (Fixed)" and right_sup == "وثاقة (Fixed)":
        M = (wu * L * x / 2) - (wu * x**2 / 2) - (wu * L**2 / 12)
        V = wu * (L/2 - x)
        R1, R2 = (wu*L/2), (wu*L/2)
        Ma, Mb = -(wu*L**2/12), -(wu*L**2/12)
    # مفصلي - مفصلي
    elif left_sup == "مفصلي (Hinged)" and right_sup == "مفصلي (Hinged)":
        M = (wu * L * x / 2) - (wu * x**2 / 2)
        V = wu * (L/2 - x)
        R1, R2 = (wu*L/2), (wu*L/2)
        Ma, Mb = 0, 0
    # وثاقة - مفصلي
    elif left_sup == "وثاقة (Fixed)" and right_sup == "مفصلي (Hinged)":
        M = (wu*x/8)*(9*L - 4*L - 4*x) # تقريبي
        # معادلة دقيقة للمسند المستمر طرف واحد
        R1 = 5/8 * wu * L
        R2 = 3/8 * wu * L
        Ma = -(wu*L**2/8)
        V = R1 - wu*x
        M = R1*x - (wu*x**2/2) + Ma
        Mb = 0
    # كابولي (وثاقة من اليسار وحر من اليمين)
    elif left_sup == "وثاقة (Fixed)" and right_sup == "كابولي (Free)":
        M = -(wu * (L - x)**2) / 2
        V = wu * (L - x)
        R1, R2 = (wu*L), 0
        Ma, Mb = -(wu*L**2/2), 0
    else:
        st.warning("هذه الجملة غير مستقرة أو تحتاج إعدادات خاصة")
        return None
    return x, M, V, R1, R2, Ma, Mb

results = analyze()

if results:
    x, M, V, R1, R2, Ma, Mb = results
    
    # 5. عرض المخططات والنتائج
    st.divider()
    col_res, col_plt = st.columns([1, 2])
    
    with col_res:
        st.subheader("📊 ردود الأفعال (Reactions)")
        st.markdown(f"<div class='support-box'>RA = {R1:.2f} t<br>RB = {R2:.2f} t</div>", unsafe_allow_html=True)
        if Ma != 0: st.info(f"عزم الوثاقة الأيسر MA = {Ma:.2f} t.m")
        if Mb != 0: st.info(f"عزم الوثاقة الأيمن MB = {Mb:.2f} t.m")
        
        # حساب الحديد
        d = h - 5
        max_m = np.max(np.abs(M))
        As = (max_m * 10**5) / (0.87 * fy * d)
        n_bars = int(np.ceil(As / (np.pi*(phi/10)**2/4)))
        st.success(f"📍 التسليح المطلوب: {max(n_bars, 2)} T{phi}")

    with col_plt:
        st.subheader("📈 مخططات القوى (Internal Forces)")
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        # رسم العزم
        ax1.plot(x, M, color='#38bdf8', lw=2)
        ax1.fill_between(x, M, color='#38bdf8', alpha=0.2)
        ax1.invert_yaxis() # العزم يرسم لأسفل في الهندسة
        ax1.set_title("Bending Moment Diagram (M)", color='white')
        ax1.grid(alpha=0.3)
        
        # رسم القص
        ax2.plot(x, V, color='#a8eb12', lw=2)
        ax2.fill_between(x, V, color='#a8eb12', alpha=0.2)
        ax2.set_title("Shear Force Diagram (V)", color='white')
        ax2.grid(alpha=0.3)
        
        fig.patch.set_facecolor('#1e293b')
        for ax in [ax1, ax2]:
            ax.set_facecolor('#0f172a')
            ax.tick_params(colors='white')
        
        st.pyplot(fig)

st.divider()
st.subheader("🎨 المخططات الإنشائية وتفريد الحديد")
col_img1, col_img2 = st.columns(2)
with col_img1:
    
    st.caption("توزيع قضبان التسليح والأساور")
with col_img2:
    
    st.caption("نمذجة المساند وتوزيع ردود الأفعال")

st.markdown("<p style='text-align:center;'>Pelan Structural Pro v22 | م. بيلان عبد الكريم © 2026</p>", unsafe_allow_html=True)
