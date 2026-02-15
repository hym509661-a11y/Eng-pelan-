import streamlit as st
import numpy as np
import ezdxf
import io

# 1. التنسيق البصري الملكي (Royal Emerald & Gold)
st.set_page_config(page_title="Pelan Masterpiece v45", layout="wide")
st.markdown("""
<style>
    .stApp {
        background-image: url("https://www.transparenttextures.com/patterns/carbon-fibre.png");
        background-color: #0d1b1e;
        color: #ffffff;
    }
    .master-card {
        background: rgba(16, 44, 41, 0.9);
        border: 2px solid #d4af37;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.6);
        margin-bottom: 25px;
    }
    .result-box {
        background: #1a3c34;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #d4af37;
    }
    .gold-text { color: #d4af37; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='master-card' style='text-align:center;'><h1 style='color:#d4af37;'>Pelan Grand Masterpiece v45</h1><p class='gold-text'>محرك التصميم الإنشائي المتكامل | م. بيلان عبد الكريم</p></div>", unsafe_allow_html=True)

# 2. لوحة التحكم والمدخلات (Sidebar)
with st.sidebar:
    st.header("⚙️ مدخلات التصميم")
    elem = st.selectbox("العنصر الإنشائي:", [
        "جائز بيتون (Beam)", "أعصاب البلاطة (Ribs)", "أعمدة خرسانية", 
        "بلاطة هوردي", "بلاطة مصمتة", "خزان مياه"
    ])
    
    st.divider()
    st.subheader("📏 الأبعاد والأحمال")
    L = st.number_input("الطول L (m):", 1.0, 20.0, 5.0)
    B = st.number_input("العرض B (cm):", 10, 100, 25)
    H = st.number_input("الارتفاع H (cm):", 20, 150, 60)
    W_u = st.number_input("الحمل المصعد Wu (kN/m):", 0.0, 200.0, 30.0)
    
    st.divider()
    st.subheader("🏗️ تسليح المهندس بيلان")
    bar_count = st.number_input("عدد القضبان:", 1, 20, 4)
    bar_size = st.selectbox("القطر المستخدم (mm):", [8, 10, 12, 14, 16, 18, 20, 25])
    fy = 420  # MPa

# 3. محرك التحليل الإنشائي (Structural Physics Engine)
# حساب العزم والقص (فرضية جائز بسيط الاستناد للتبسيط البرمجي)
M_max = (W_u * L**2) / 8
V_max = (W_u * L) / 2
As_provided = bar_count * (np.pi * (bar_size/10)**2 / 4) # cm2

# 4. العرض الفني والرسومات
col1, col2 = st.columns([1.2, 1])

with col1:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader(f"📊 التحليل الإنشائي: {elem}")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.write("📉 **أقصى عزم (M max):**")
        st.markdown(f"<p class='result-box'>{M_max:.2f} kN.m</p>", unsafe_allow_html=True)
    with c2:
        st.write("📉 **أقصى قص (V max):**")
        st.markdown(f"<p class='result-box'>{V_max:.2f} kN.m</p>", unsafe_allow_html=True)
    with c3:
        st.write("🏗️ **مساحة الحديد:**")
        st.markdown(f"<p class='result-box'>{As_provided:.2f} cm²</p>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"### 👨‍🏫 توصية المهندس بيلان للـ {elem}:")
    
    if "جائز" in elem or "أعصاب" in elem:
        st.info(f"💡 المخطط يظهر تسليحاً سفلياً بقيمة {bar_count}Φ{bar_size}. تأكد من تكسيح الحديد أو وصله عند المساند حسب مخطط القص.")
        [attachment_0](attachment)
    elif "أعمدة" in elem:
        st.info("💡 دقق نسبة التسليح Rho؛ يجب أن تكون بين 1% و 4% من مساحة المقطع الخرساني.")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='master-card'>", unsafe_allow_html=True)
    st.subheader("🖋️ تفاصيل التسليح (BBS)")
    
    # محاكاة رسم مخطط الحديد مع رفع السهم
    st.write(f"🔍 **تفريش الحديد للـ {elem}:**")
    
    
    st.markdown(f"""
    <div style='border: 1px dashed #d4af37; padding: 10px;'>
        <p style='text-align:center;'>📌 <b>توصيف الحديد:</b></p>
        <p style='text-align:center;'>Bottom: {bar_count} T {bar_size} L={L+0.4}m</p>
        <p style='text-align:center; color:#50c878;'>↑ (سهم مرفوع يوضح القطر والعدد) ↑</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    if st.button("🛠️ تصدير المخطط التنفيذي (DXF) 🚀"):
        try:
            doc = ezdxf.new(setup=True); msp = doc.modelspace()
            # رسم الجائز
            msp.add_lwpolyline([(0,0), (L*10, 0), (L*10, H), (0, H), (0,0)])
            # رسم سيخ الحديد
            msp.add_line((0.5, 5), (L*10-0.5, 5), dxfattribs={'color': 1})
            # إضافة نص السهم
            msp.add_text(f"{bar_count}%%c{bar_size}", dxfattribs={'height': 2}).set_placement((L*5, 7))
            
            buf = io.StringIO(); doc.write(buf)
            st.download_button("📥 تحميل المخطط للأوتوكاد", buf.getvalue(), f"Pelan_Detail_{elem}.dxf")
            st.success("تم الحساب والتصدير بدقة!")
        except Exception as e:
            st.error(f"خطأ: {e}")
            
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37;'>Pelan Engine v45 | م. بيلان عبد الكريم | 2026</p>", unsafe_allow_html=True)
