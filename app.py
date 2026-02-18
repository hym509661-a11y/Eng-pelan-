import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 1. إعدادات الواجهة والختم (بدون أي تغيير)
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

# 2. القائمة الجانبية (إضافة خيارات المساند مع الحفاظ على البقية)
with st.sidebar:
    st.header("⚙️ الإعدادات الهندسية")
    L = st.number_input("طول البحر L (m):", 1.0, 20.0, 6.0)
    wu = st.number_input("الحمل Wu (t/m):", 0.1, 50.0, 3.0)
    
    st.divider()
    st.subheader("📍 تحديد نوع المساند")
    left_sup = st.selectbox("المسند الأيسر (A):", ["وثاقة (Fixed)", "مفصلي (Hinged)", "متحرك (Roller)"])
    right_sup = st.selectbox("المسند الأيمن (B):", ["وثاقة (Fixed)", "مفصلي (Hinged)", "متحرك (Roller)", "ظفر (Cantilever)"])
    
    st.divider()
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    h = st.number_input("الارتفاع h (cm):", 10, 200, 60)
    phi_main = st.selectbox("قطر التسليح الرئيسي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    phi_extra = st.selectbox("قطر التسليح الإضافي (mm):", [10, 12, 14, 16], index=1)
    fy = 4000

# 3. محرك التحليل الإنشائي المطوّر
def analyze_engine():
    x = np.linspace(0, L, 500)
    is_cantilever = (right_sup == "ظفر (Cantilever)")
    
    if is_cantilever:
        M = -(wu * (L - x)**2) / 2
        V = wu * (L - x)
        R1, R2 = (wu * L), 0
        iron_mode = "top"
    elif "وثاقة" in left_sup and "وثاقة" in right_sup:
        M = (wu*L*x/2) - (wu*x**2/2) - (wu*L**2/12)
        V = wu*(L/2 - x)
        R1 = R2 = wu*L/2
        iron_mode = "bottom"
    else: # مساند بسيطة
        M = (wu*L*x/2) - (wu*x**2/2)
        V = wu*(L/2 - x)
        R1 = R2 = wu*L/2
        iron_mode = "bottom"
    return x, M, V, R1, R2, iron_mode

res = analyze_engine()
if res:
    x, M, V, R1, R2, iron_mode = res
    d = h - 5
    max_m = np.max(np.abs(M))
    
    # حساب التسليح
    As_req = (max_m * 10**5) / (0.87 * fy * d)
    n_main = max(int(np.ceil(As_req / (np.pi*(phi_main/10)**2/4))), 2)
    n_top_hangers = 2
    n_extra = 2 if L > 5 else 0

    # 4. العرض (Tabs)
    tab1, tab2 = st.tabs(["📈 التحليل الإنشائي", "🏗️ المخططات التنفيذية"])

    with tab1:
        col_res, col_plt = st.columns([1, 2])
        with col_res:
            st.subheader("📊 ردود الأفعال")
            st.info(f"RA = {R1:.2f} t | RB = {R2:.2f} t")
            st.success(f"التسليح الرئيسي: {n_main} T{phi_main}")
        with col_plt:
            fig_an, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 5))
            ax1.plot(x, M, color='#38bdf8'); ax1.fill_between(x, M, alpha=0.2, color='#38bdf8'); ax1.invert_yaxis()
            ax2.plot(x, V, color='#a8eb12'); ax2.fill_between(x, V, alpha=0.2, color='#a8eb12')
            for ax in [ax1, ax2]: ax.set_facecolor('#0f172a'); fig_an.patch.set_facecolor('#0f172a'); ax.tick_params(colors='white')
            st.pyplot(fig_an)

    with tab2:
        col_long, col_cross = st.columns([2, 1])
        with col_long:
            st.subheader("تفريد الحديد (Longitudinal Section)")
            fig_l, ax_l = plt.subplots(figsize=(10, 4))
            ax_l.set_aspect('equal')
            L_cm = L*100; cov = 5
            
            # رسم البيتون والمساند
            ax_l.add_patch(patches.Rectangle((0, 0), L_cm, h, color='#334155', alpha=0.4))
            ax_l.plot([0, 0], [-10, h+10], color='white', lw=3 if "وثاقة" in left_sup else 1)
            if right_sup != "ظفر (Cantilever)":
                ax_l.plot([L_cm, L_cm], [-10, h+10], color='white', lw=3 if "وثاقة" in right_sup else 1)

            # الحديد الرئيسي (سفلي أو علوي حسب الحالة)
            y_main = (h-cov) if iron_mode == "top" else cov
            ax_l.plot([cov, L_cm-cov], [y_main, y_main], color='#38bdf8', lw=3)
            # عكفات
            h_dir = -10 if iron_mode == "top" else 10
            ax_l.plot([cov, cov], [y_main, y_main+h_dir], color='#38bdf8', lw=3)
            ax_l.plot([L_cm-cov, L_cm-cov], [y_main, y_main+h_dir], color='#38bdf8', lw=3)
            ax_l.text(L_cm/2, y_main+(12 if iron_mode=="top" else -15), f"{n_main} T {phi_main} (Main)", color='#38bdf8', ha='center', weight='bold')

            # الحديد الثانوي
            y_sec = cov if iron_mode == "top" else (h-cov)
            ax_l.plot([cov, L_cm-cov], [y_sec, y_sec], color='#94a3b8', lw=1.5)
            ax_l.text(L_cm/2, y_sec+(10 if iron_mode=="bottom" else -12), f"{n_top_hangers} T 12 (Secondary)", color='#94a3b8', ha='center')

            # الأساور (الكانات)
            for s_x in range(15, int(L_cm), 20):
                ax_l.plot([s_x, s_x], [cov, h-cov], color='#ef4444', lw=1, alpha=0.5)
            ax_l.text(L_cm*0.8, h/2, f"Stirrups T8 @ 20cm", color='#ef4444', rotation=90, fontsize=8)

            ax_l.axis('off'); fig_l.patch.set_facecolor('#0f172a'); st.pyplot(fig_l)

        with col_cross:
            st.subheader("المقطع العرضي")
            fig_c, ax_c = plt.subplots(figsize=(5, 6))
            ax_c.set_aspect('equal')
            ax_c.add_patch(patches.Rectangle((0, 0), B, h, edgecolor='white', facecolor='#1e293b', lw=2))
            ax_c.add_patch(patches.Rectangle((3, 3), B-6, h-6, edgecolor='#ef4444', facecolor='none', ls='--'))
            
            # توزيع الحديد في المقطع
            y_m = h-6 if iron_mode == "top" else 6
            y_s = 6 if iron_mode == "top" else h-6
            sp = (B-10)/(n_main-1) if n_main > 1 else 0
            for i in range(n_main): ax_c.add_patch(plt.Circle((5+i*sp, y_m), phi_main/10, color='#38bdf8'))
            for i in range(2): ax_c.add_patch(plt.Circle((5+i*(B-10), y_s), 0.6, color='#94a3b8'))
            
            ax_c.axis('off'); fig_c.patch.set_facecolor('#0f172a'); st.pyplot(fig_c)

# 5. الختم الرسمي (المهندس المدني بيلان مصطفى عبدالكريم)
st.markdown(f"""
    <div class="footer-stamp">
        <h2 style="color: #38bdf8; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 1.2em; margin:5px 0;">دراسات - إشراف - تعهدات</p>
        <h3 style="color: #ffffff; letter-spacing: 2px;">0998449697</h3>
        <p style="color: #64748b;">Pelan Structural Pro v22 | © 2026</p>
    </div>
""", unsafe_allow_html=True)
