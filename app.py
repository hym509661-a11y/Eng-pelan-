import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. إعدادات الواجهة
st.set_page_config(page_title="Pelan Structural Pro", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    .header-box {
        background: linear-gradient(90deg, #1e293b, #334155);
        padding: 20px; border-radius: 15px; border: 1px solid #38bdf8;
        text-align: center; margin-bottom: 25px;
    }
    .footer-stamp {
        text-align: center; border: 2px solid #38bdf8; 
        padding: 15px; border-radius: 15px; margin-top: 50px;
        background-color: #1e293b;
    }
    </style>
    <div class="header-box">
        <h1 style='color: #38bdf8; margin:0;'>Pelan Structural Analysis Pro</h1>
        <p style='color: #94a3b8;'>نظام التحليل والنمذجة الديناميكية | م. بيلان عبد الكريم</p>
    </div>
""", unsafe_allow_html=True)

# 2. المدخلات في القائمة الجانبية
with st.sidebar:
    st.header("⚙️ الإعدادات الهندسية")
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 6.0)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 3.0)
    st.divider()
    B = st.number_input("عرض المقطع B (cm):", 20, 100, 30)
    h = st.number_input("ارتفاع المقطع h (cm):", 10, 200, 60)
    phi = st.selectbox("قطر التسليح الرئيسي (mm):", [12, 14, 16, 18, 20, 25])
    left_sup = st.radio("المسند الأيسر:", ["وثاقة (Fixed)", "مفصلي (Hinged)"])
    right_sup = st.radio("المسند الأيمن:", ["وثاقة (Fixed)", "مفصلي (Hinged)", "كابولي (Free)"])

# 3. محرك التحليل (Structural Engine)
fy = 4000
def analyze():
    x = np.linspace(0, L, 500)
    if left_sup == "وثاقة (Fixed)" and right_sup == "وثاقة (Fixed)":
        M = (wu * L * x / 2) - (wu * x**2 / 2) - (wu * L**2 / 12)
        V = wu * (L/2 - x)
        R1 = R2 = wu*L/2
    elif left_sup == "مفصلي (Hinged)" and right_sup == "مفصلي (Hinged)":
        M = (wu * L * x / 2) - (wu * x**2 / 2)
        V = wu * (L/2 - x)
        R1 = R2 = wu*L/2
    else: # حالة افتراضية للتبسيط
        M = (wu * L * x / 2) - (wu * x**2 / 2)
        V = wu * (L/2 - x)
        R1 = R2 = wu*L/2
    return x, M, V, R1, R2

res = analyze()
if res:
    x, M, V, R1, R2 = res
    d = h - 5
    max_m = np.max(np.abs(M))
    As = (max_m * 10**5) / (0.87 * fy * d)
    n_bars = max(int(np.ceil(As / (np.pi*(phi/10)**2/4))), 2)

    # --- العرض الجرافيكي ---
    tab1, tab2 = st.tabs(["📈 التحليل الإنشائي", "🏗️ المخططات التنفيذية"])

    with tab1:
        fig_an, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6))
        ax1.fill_between(x, M, color='#38bdf8', alpha=0.3)
        ax1.set_title("Bending Moment (M)", color='white')
        ax1.invert_yaxis()
        ax2.fill_between(x, V, color='#a8eb12', alpha=0.3)
        ax2.set_title("Shear Force (V)", color='white')
        for ax in [ax1, ax2]:
            ax.set_facecolor('#0f172a')
            fig_an.patch.set_facecolor('#0f172a')
            ax.tick_params(colors='white')
        st.pyplot(fig_an)

    with tab2:
        col_long, col_cross = st.columns([2, 1])

        with col_long:
            st.subheader("تفريد الحديد (Longitudinal Section)")
            fig_l, ax_l = plt.subplots(figsize=(10, 4))
            ax_l.set_aspect('equal')
            
            # رسم الجائز
            beam_rect = patches.Rectangle((0, 0), L*100, h, color='#334155', alpha=0.5)
            ax_l.add_patch(beam_rect)
            
            # رسم الحديد السفلي مع العكفات
            cov = 5
            hook = 10
            # الخط الرئيسي
            ax_l.plot([cov, L*100-cov], [cov, cov], color='#38bdf8', lw=3, label=f"{n_bars}T{phi}")
            # العكفات
            ax_l.plot([cov, cov], [cov, cov+hook], color='#38bdf8', lw=3)
            ax_l.plot([L*100-cov, L*100-cov], [cov, cov+hook], color='#38bdf8', lw=3)
            
            # رسم الحديد العلوي (علاقات أساور)
            ax_l.plot([cov, L*100-cov], [h-cov, h-cov], color='#94a3b8', lw=1.5)
            
            # رسم الأساور (Stirrups) بشكل تكراري
            stirrup_space = 20 # كل 20 سم
            for s_pos in range(10, int(L*100), stirrup_space):
                ax_l.plot([s_pos, s_pos], [cov, h-cov], color='#ef4444', lw=1, alpha=0.6)

            ax_l.set_xlim(-50, L*100+50)
            ax_l.set_ylim(-20, h+20)
            ax_l.axis('off')
            fig_l.patch.set_facecolor('#0f172a')
            st.pyplot(fig_l)
            

        with col_cross:
            st.subheader("المقطع العرضي (Cross Section)")
            fig_c, ax_c = plt.subplots(figsize=(5, 6))
            ax_c.set_aspect('equal')
            
            # الخرسانة والأساور
            ax_c.add_patch(patches.Rectangle((0, 0), B, h, edgecolor='white', facecolor='#1e293b', lw=2))
            ax_c.add_patch(patches.Rectangle((3, 3), B-6, h-6, edgecolor='#ef4444', facecolor='none', ls='--'))
            
            # توزيع الحديد السفلي
            spacing = (B-10)/(n_bars-1) if n_bars > 1 else 0
            for i in range(n_bars):
                ax_c.add_patch(plt.Circle((5 + i*spacing, 6), phi/10, color='#38bdf8'))
            
            ax_c.set_xlim(-5, B+5)
            ax_c.set_ylim(-5, h+5)
            ax_c.axis('off')
            fig_c.patch.set_facecolor('#0f172a')
            st.pyplot(fig_c)
            

# 4. الختم الرسمي
st.markdown(f"""
    <div class="footer-stamp">
        <h2 style="color: #38bdf8; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 1.2em; margin:5px 0;">دراسات - إشراف - تعهدات</p>
        <h3 style="color: #ffffff; letter-spacing: 2px;">0998449697</h3>
        <p style="color: #64748b;">Pelan Structural Pro v22 | © 2026</p>
    </div>
""", unsafe_allow_html=True)
