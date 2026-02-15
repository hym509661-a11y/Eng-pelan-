import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import ezdxf
import io

# 1. إعدادات الهوية
ST_NAME, ST_JOB = "بيلان مصطفى عبد الكريم", "المهندس المدني"

st.set_page_config(page_title="Pelan Giant v85", layout="wide")
st.markdown("""
<style>
    .stApp { background-color: #0b1619; color: white; }
    .main-panel { background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }
    .cad-box { background: #1a1c23; border: 2px solid #333; padding: 15px; border-radius: 10px; color: #50c878; margin: 15px 0; }
    .stamp { border: 4px double #d4af37; padding: 10px; width: 280px; text-align: center; background: white; color: black; float: left; }
</style>
""", unsafe_allow_html=True)

# 2. المدخلات (Sidebar)
with st.sidebar:
    st.header("🏗️ مدخلات التصميم التفصيلية")
    B = st.number_input("العرض B (cm):", 20, 100, 30)
    H = st.number_input("الارتفاع H (cm):", 20, 200, 60)
    L = st.number_input("البحر L (m):", 1.0, 20.0, 5.0)
    W = st.number_input("الحمل الموزع W (kN/m):", 1.0, 500.0, 30.0)
    phi_main = st.selectbox("قطر الحديد السفلي:", [12, 14, 16, 18, 20, 25])
    phi_top = st.selectbox("قطر الحديد العلوي (تعليق):", [10, 12, 14, 16])
    phi_stir = st.selectbox("قطر الكانات:", [8, 10, 12])

# 3. المحرك الإنشائي (Calculations)
M_max = (W * L**2) / 8
V_max = (W * L) / 2
d = H - 5 # الغطاء الخرساني

# حساب الحديد السفلي (Main Steel)
As_main = (M_max * 1e6) / (0.87 * 420 * d * 10)
n_main = max(2, int(np.ceil(As_main / (np.pi * phi_main**2 / 4))))

# حساب الحديد العلوي (Top/Stirrup Hangers)
n_top = 2 # كحد أدنى لتعليق الكانات

# حساب الكانات (Shear)
s_spacing = 15 # تقسيط افتراضي 15 سم

# 4. واجهة العرض (The Master Layout)
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏗️ Pelan Structural Giant - Analysis & Design</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='main-panel'>", unsafe_allow_html=True)
    st.subheader("📝 المذكرة الحسابية التفصيلية")
    st.write(f"**أقصى عزم (M max):** {M_max:.2f} kNm")
    st.write(f"**أقصى قص (V max):** {V_max:.2f} kN")
    st.divider()
    st.write(f"✅ **التسليح السفلي:** {n_main} T {phi_main}")
    st.write(f"✅ **التسليح العلوي:** {n_top} T {phi_top}")
    st.write(f"✅ **الكانات:** Φ {phi_stir} @ {s_spacing} cm")
    
    # رسم مخطط العزم والقص
    st.subheader("📈 مخططات القوى (Moment & Shear)")
    x = np.linspace(0, L, 100)
    shear = W * (L/2 - x)
    moment = (W*x/2) * (L - x)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 6))
    ax1.fill_between(x, shear, color='skyblue', alpha=0.4)
    ax1.set_title("Shear Force Diagram (SFD)")
    ax2.fill_between(x, moment, color='orange', alpha=0.4)
    ax2.set_title("Bending Moment Diagram (BMD)")
    plt.tight_layout()
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-box'>", unsafe_allow_html=True)
    st.subheader("🖋️ المخطط التفصيلي للحديد (Detailing)")
    st.write(f"مقطع عرضي في الجائز B={B}cm, H={H}cm")
    
    # رسم المقطع العرضي للحديد
    
    
    st.write(f"**تفصيل الفرش:** يتم توزيع {n_main} قضبان في طبقة واحدة مع غطاء 3سم.")
    st.write(f"**التعليق:** قضبان علوية عدد {n_top} لربط الكانات.")
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الهندسي
    st.markdown(f"""
    <div class='stamp'>
        <p style='margin:0;'><b>{ST_JOB}</b></p>
        <p style='color:#d4af37; font-size:18px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:12px;'>دراسة - إشراف - تعهدات</p>
        <hr style='border:1px solid #d4af37;'>
        <p style='font-size:10px;'>ختم الاعتماد المهني 2026</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

# أزرار التصدير
st.divider()
if st.button("🚀 تصدير المخطط الكامل إلى AutoCAD"):
    doc = ezdxf.new(setup=True); msp = doc.modelspace()
    msp.add_text(f"BEAM DESIGN - ENG. PELAN", dxfattribs={'height': 5})
    buf = io.StringIO(); doc.write(buf)
    st.download_button("📥 تحميل ملف DXF", buf.getvalue(), "Structural_Pelan.dxf")
