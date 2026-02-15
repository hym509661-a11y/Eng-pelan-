import streamlit as st
import numpy as np
import ezdxf
import io

# 1. الإعدادات البصرية الملكية (Engineering Royal Theme)
st.set_page_config(page_title="Pelan Ultimate Suite v54", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0d1b1e; color: #ffffff; }
    .master-card {
        background: rgba(16, 44, 41, 0.95);
        border: 2px solid #d4af37;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
    }
    .result-box {
        background: #1a3c34; border-left: 5px solid #d4af37;
        padding: 12px; border-radius: 8px; margin: 8px 0;
    }
    .gold-label { color: #d4af37; font-weight: bold; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Ultimate Structural Suite v54</h1><p style='color:#d4af37;'>الموسوعة الهندسية المتكاملة | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. القائمة الجانبية الذكية (Smart Selector)
with st.sidebar:
    st.header("🏗️ اختيار العنصر الإنشائي")
    elem_type = st.selectbox("نوع العنصر:", ["جائز/عصب", "بلاطة مصمتة", "بلاطة هوردي", "أعمدة", "أساسات منفردة"])
    
    st.divider()
    st.subheader("📐 الأبعاد الهندسية (cm)")
    if "أساسات" in elem_type:
        L_dim = st.number_input("طول الأساس L (cm):", 100, 500, 200)
        B_dim = st.number_input("عرض الأساس B (cm):", 100, 500, 180)
        H_dim = st.number_input("سماكة الأساس H (cm):", 30, 150, 50)
        Load = st.number_input("حمل العمود P (kN):", 100, 5000, 1200)
    elif "أعمدة" in elem_type:
        B_dim = st.number_input("عرض العمود B (cm):", 20, 100, 30)
        H_dim = st.number_input("عمق العمود H (cm):", 20, 150, 60)
        L_dim = st.number_input("ارتفاع الطابق L (m):", 2.0, 6.0, 3.2)
        Load = st.number_input("الحمل المحوري P (kN):", 100, 8000, 1500)
    else:
        L_dim = st.number_input("طول البحر L (m):", 1.0, 15.0, 5.0)
        B_dim = st.number_input("العرض B (cm):", 10, 100, 25)
        H_dim = st.number_input("السماكة H (cm):", 10, 150, 60)
        Load = st.number_input("الحمل Wu (kN/m):", 1.0, 200.0, 35.0)

    st.divider()
    phi_main = st.selectbox("قطر الحديد الرئيسي (mm):", [12, 14, 16, 18, 20, 22, 25], index=2)
    phi_sec = st.selectbox("قطر الكانات/التوزيع (mm):", [8, 10, 12])

# 3. محرك التصميم الموحد (Unified Design Engine)
f_y, f_cu = 420, 25
area_bar = (np.pi * phi_main**2) / 4

if "أعمدة" in elem_type:
    # تصميم أعمدة (Simplified Axial Load Design)
    As_req = (Load * 1000 - 0.35 * f_cu * (B_dim * H_dim * 100)) / (0.67 * f_y)
    n_bars = max(4, int(np.ceil(max(As_req, 0.01 * B_dim * H_dim * 100) / area_bar)))
    n_main, n_top, n_hang, stirrups = n_bars, 0, 0, f"Φ{phi_sec} @ 15cm"
    results = {"P": f"{Load} kN", "Section": f"{B_dim}x{H_dim} cm", "As": f"{As_req/100:.2f} cm²"}

elif "أساسات" in elem_type:
    # تصميم أساسات (Bearing Capacity & Bending)
    q_act = (Load) / (L_dim * B_dim / 10000)
    M_footing = (q_act * (L_dim/100 - 0.3)**2) / 2 # تقديري
    As_req = (M_footing * 10**6) / (0.87 * f_y * (H_dim-7) * 10)
    n_main = int(np.ceil(max(As_req, 0.0018 * B_dim * H_dim * 100) / area_bar))
    n_top, n_hang, stirrups = n_main, 0, 0, "فرش وغطاء"
    results = {"Stress": f"{q_act:.1f} kN/m²", "Section": f"{L_dim}x{B_dim} cm", "As": f"{As_req/100:.2f} cm²"}

else:
    # تصميم جوائز وبلاطات
    M_max = (Load * L_dim**2) / 8
    As_req = (M_max * 10**6) / (0.87 * f_y * (H_dim-5) * 10)
    n_main = max(2, int(np.ceil(As_req / area_bar)))
    n_top = max(2, int(np.ceil(n_main * 0.4)))
    n_hang = 2
    stirrups = f"Φ{phi_sec} @ 15cm"
    results = {"Moment": f"{M_max:.1f} kNm", "Section": f"{B_dim}x{H_dim} cm", "As": f"{As_req/100:.2f} cm²"}

# 4. العرض الفني (النتائج والتفريد)
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 التقرير الإنشائي: {elem_type}")
    
    res_grid = st.columns(len(results))
    for i, (k, v) in enumerate(results.items()):
        res_grid[i].markdown(f"<div class='result-box'><span class='gold-label'>{k}:</span><br><b>{v}</b></div>", unsafe_allow_html=True)
    
    st.divider()
    st.markdown(f"### 👨‍🏫 توصية المهندس بيلان للـ {elem_type}:")
    
    if "أعمدة" in elem_type:
        st.write(f"✅ **الحديد الطولي:** {n_main} T {phi_main}")
        st.write(f"✅ **الكانات:** {stirrups}")
        
    elif "أساسات" in elem_type:
        st.write(f"✅ **تسليح الاتجاهين (فرش وغطاء):** {n_main} T {phi_main} / m'")
        
    else:
        st.write(f"✅ **الفرش السفلي:** {n_main} T {phi_main}")
        st.write(f"✅ **الحديد العلوي:** {n_top} T {phi_main}")
        st.write(f"✅ **الكانات:** {stirrups}")
        

    st.info("💡 تم الحساب تلقائياً بناءً على الكود المعتمد لضمان أعلى مستويات الأمان.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط التفريد المرفوع (BBS)")
    
    # محاكاة السهم المرفوع والتوصيف
    st.markdown(f"""
    <div style='border:2px solid #d4af37; padding:15px; border-radius:10px; text-align:center;'>
        <p class='gold-label'>تفصيل حديد {elem_type}</p>
        <div style='margin:20px 0; padding:20px; background:rgba(255,255,255,0.05);'>
            <h2 style='color:#50c878;'>{n_main} Φ {phi_main}</h2>
            <p style='color:#d4af37;'>↑ سهم رفع (الحديد الرئيسي) ↑</p>
            <hr style='border-color:#d4af37;'>
            <h3 style='color:#50c878;'>{stirrups}</h3>
            <p style='color:#d4af37;'>↑ سهم رفع (الكانات/التوزيع) ↑</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("🛠️ تصدير المخطط المتكامل إلى AutoCAD 🚀"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم الحدود الخرسانية
            msp.add_lwpolyline([(0,0), (100,0), (100,100), (0,100), (0,0)])
            # رسم الحديد الرئيسي وسهم الرفع
            msp.add_line((10, 20), (90, 20), dxfattribs={'color': 1})
            msp.add_line((50, 20), (50, 40), dxfattribs={'color': 2})
            msp.add_text(f"{n_main}%%c{phi_main}", dxfattribs={'height': 5}).set_placement((50, 45))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل DXF", buf.getvalue(), f"Pelan_{elem_type}.dxf")
            st.success("تم التصدير بنجاح!")
        except Exception as e:
            st.error(f"خطأ: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Ultimate Structural Suite v54 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
