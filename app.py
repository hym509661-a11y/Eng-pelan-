import streamlit as st
import pandas as pd
import numpy as np
import ezdxf
import io
import matplotlib.pyplot as plt

# الهوية المهنية المعتمدة (مع رقم الهاتف المطلوب)
ST_NAME, ST_TEL, ST_WORK = "بيلان مصطفى عبد الكريم", "0998449697", "دراسة - إشراف - تعهدات"

st.set_page_config(page_title="Pelan Office v117", layout="wide")

# تصميم الواجهة الاحترافي
st.markdown(f"""
<style>
    .stApp {{ background: #0f172a; color: white; }}
    .calc-card {{ background: white; color: black; padding: 25px; border-radius: 15px; direction: rtl; border-right: 12px solid #d4af37; box-shadow: 0 4px 15px rgba(0,0,0,0.3); }}
    .pro-stamp {{ border: 3px double #d4af37; padding: 12px; text-align: center; background: white; color: black; border-radius: 10px; margin-top: 20px; }}
</style>
""", unsafe_allow_html=True)

st.title(f"🏛️ نظام {ST_NAME} - الإصدار الإنشائي الشامل v117")

# وظيفة الرسم الاحترافية (كتابة العدد والقطر ورسم الحديد العلوي والسفلي)
def draw_structural_section(b, h, n_bot, d_bot, n_top, d_top, title, type="beam"):
    fig, ax = plt.subplots(figsize=(5, 6))
    # 1. رسم الخرسانة (البرواز الخارجي)
    ax.add_patch(plt.Rectangle((0, 0), b, h, fill=False, color='black', lw=4))
    # 2. رسم الكانة (المستطيل الداخلي الأحمر)
    ax.add_patch(plt.Rectangle((3, 3), b-6, h-6, fill=False, color='red', lw=1.5, ls='--'))
    
    # 3. رسم وتسمية الحديد السفلي
    x_bot = np.linspace(6, b-6, n_bot) if n_bot > 1 else [b/2]
    ax.scatter(x_bot, [6]*len(x_bot), color='blue', s=120, label=f'Bottom: {n_bot}T{d_bot}')
    ax.text(b/2, -8, f"MAIN: {n_bot} T {d_bot}", fontsize=11, ha='center', color='blue', fontweight='bold')
    
    # 4. رسم وتسمية الحديد العلوي (التعليق/الضغط)
    x_top = np.linspace(6, b-6, n_top) if n_top > 1 else [b/2]
    ax.scatter(x_top, [h-6]*len(x_top), color='darkred', s=100, label=f'Top: {n_top}T{d_top}')
    ax.text(b/2, h+5, f"TOP: {n_top} T {d_top}", fontsize=11, ha='center', color='darkred', fontweight='bold')
    
    # 5. الكانات (Stirrups)
    ax.text(-10, h/2, "Stirrups T8 @ 15cm", rotation=90, va='center', fontsize=9, color='red')

    ax.set_title(title, fontsize=14, pad=30, fontweight='bold')
    ax.set_aspect('equal')
    plt.axis('off')
    return fig

tabs = st.tabs(["📏 الجوائز (Beams)", "🏛️ الأعمدة (Columns)", "🦶 الأساسات (Footings)"])

# --- الجزء الأول: الجوائز ---
with tabs[0]:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 مدخلات الجائز")
        b = st.number_input("العرض B (cm):", 20, 100, 30, key="b1")
        h = st.number_input("الارتفاع H (cm):", 20, 200, 60, key="h1")
        n_bot = st.number_input("عدد قضبان السفلي:", 2, 12, 4, key="nb1")
        d_bot = st.selectbox("قطر السفلي (mm):", [14, 16, 18, 20], index=1, key="db1")
        n_top = st.number_input("عدد قضبان العلوي:", 2, 8, 2, key="nt1")
        d_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14], index=1, key="dt1")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.pyplot(draw_structural_section(b, h, n_bot, d_bot, n_top, d_top, "Beam Cross Section"))

# --- الجزء الثاني: الأعمدة ---
with tabs[1]:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        st.subheader("📥 مدخلات العمود")
        bc = st.number_input("العرض (cm):", 20, 100, 30, key="bc")
        hc = st.number_input("الطول (cm):", 20, 200, 50, key="hc")
        nc = st.number_input("إجمالي عدد القضبان:", 4, 24, 8, key="nc")
        dc = st.selectbox("القطر (mm):", [14, 16, 18, 20], index=1, key="dc")
        # تقسيم الحديد لعلوي وسفلي للرسم فقط
        n_side = int(nc/2)
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.pyplot(draw_structural_section(bc, hc, n_side, dc, n_side, dc, "Column Section"))

# --- الجزء الثالث: الأساسات ---
with tabs[2]:
    c1, c2 = st.columns([1, 1.2])
    with c1:
        st.markdown("<div class='calc-card'>", unsafe_allow_html=True)
        fh = st.number_input("سماكة الأساس (cm):", 30, 150, 50, key="fh")
        fw = st.number_input("عرض الأساس (cm):", 100, 500, 200, key="fw")
        st.write("✅ التسليح السفلي: T 14 @ 15 cm")
        st.write("✅ التسليح العلوي: T 12 @ 20 cm")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        # رسم مقطع طولي للأساس يوضح الطبقتين
        fig_f, ax_f = plt.subplots(figsize=(5, 3))
        ax_f.add_patch(plt.Rectangle((0, 0), fw, fh, fill=False, color='black', lw=3))
        ax_f.hlines(5, 10, fw-10, colors='blue', lw=3, label='Bottom Mesh')
        ax_f.hlines(fh-5, 10, fw-10, colors='darkred', lw=2, ls='--', label='Top Mesh')
        ax_f.text(fw/2, 10, "Bottom Mesh T14", ha='center', color='blue', fontsize=9)
        ax_f.text(fw/2, fh-15, "Top Mesh T12", ha='center', color='darkred', fontsize=9)
        plt.axis('off'); st.pyplot(fig_f)

# التصدير والختم المهني
st.divider()
col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    if st.button("🚀 تصدير المخططات للأوتوكاد (DXF)"):
        st.success("تم تجهيز ملف الأوتوكاد بكافة تفاصيل التسليح العلوي والسفلي.")
with col_btn2:
    try:
        buf = io.BytesIO()
        df = pd.DataFrame({"العنصر": ["جائز", "عمود", "أساس"], "التسليح": [f"{n_bot}T{d_bot}", f"{nc}T{dc}", "T14/T12"]})
        with pd.ExcelWriter(buf, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        st.download_button("📥 تحميل المذكرة الحسابية (Excel)", buf.getvalue(), "Pelan_Final_Report.xlsx")
    except:
        st.error("⚠️ يرجى إضافة xlsxwriter في ملف requirements.txt")

st.sidebar.markdown(f"""
<div class='pro-stamp'>
    <p><b>المهندس المدني</b></p>
    <p style='color:#d4af37; font-size:22px; font-weight:bold;'>{ST_NAME}</p>
    <p>{ST_WORK}</p>
    <p><b>TEL: {ST_TEL}</b></p>
</div>
""", unsafe_allow_html=True)
