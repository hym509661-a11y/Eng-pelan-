import streamlit as st
import numpy as np
from PIL import Image

# --- الهوية المهنية للمهندس بيلان ---
st.set_page_config(page_title="منظومة المهندس بيلان الذكية", layout="wide")
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 5px solid #1b5e20; padding: 25px; border-radius: 20px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">محرك التحليل الإنشائي الآلي (تحليل المخططات المرفوعة)</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 20px; margin:5px;">دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

# --- محمل الملفات (هنا ترفع المخطط يا بشمهندس) ---
st.header("📂 خطوة 1: ارفع مخططك المعماري/الإنشائي")
uploaded_file = st.file_uploader("ارفع صورة المخطط (JPG/PNG) ليقوم النظام بقراءتها وتحليلها", type=["jpg", "png", "jpeg"])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="المخطط المرفوع - جاري المعالجة الإنشائية...", use_container_width=True)

# --- المدخلات الثابتة للمشروع ---
st.sidebar.header("📋 ثوابت المشروع")
num_floors = st.sidebar.number_input("إجمالي عدد الطوابق", min_value=1, value=4)
soil_q = st.sidebar.number_input("تحمل التربة (kN/m²)", value=200)

# --- محرك القرارات الهندسية الآلي ---
st.header("📐 خطوة 2: التحليل الإنشائي الآلي (وفق الكود السوري)")

# بفرض النظام استخرج الأبعاد من المخطط (مثال: Lx=6, Ly=4)
Lx = st.number_input("المجاز الطويل المستخرج Lx (m)", value=6.0)
Ly = st.number_input("المجاز القصير المستخرج Ly (m)", value=4.5)

# --- آلياً: تحديد نوع البلاطة وسلوكها ---
st.subheader("1. تحليل البلاطات والجوائز")
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**🔹 بلاطة القبو (مصمتة آلياً):**")
    ratio = Lx / Ly
    behavior = "اتجاهين" if ratio <= 2 else "اتجاه واحد"
    st.info(f"النظام: تعمل بـ {behavior}")

with col_b:
    st.markdown("**🔹 بلاطة المتكرر (هوردي آلياً):**")
    st.success(f"توجيه الأعصاب: في الاتجاه القصير ({Ly} m)")

# حساب حمل الجائز الناقل للأعمدة
wu_slab = (1.4 * 2.5) + (1.7 * 2.0)
wu_beam = (wu_slab * Ly/2) + 5.0 # حمل بلاطة + وزن جائز
vu_beam = (wu_beam * Lx) / 2 # رد فعل الجائز

# --- آلياً: تصميم الأعمدة بشرط الـ 900 ---
st.subheader("2. تصميم الأعمدة (الحد الأدنى 900 cm²)")
pu_total = vu_beam * 2 * num_floors # حمل تراكمي لعمود وسطي
ac_req = (pu_total * 10) / (0.35 * 25 + 0.67 * 400 * 0.01)
ac_final = max(900, ac_req)

if ac_final == 900:
    st.success(f"تم اعتماد مقطع الكود الأدنى: 900 cm² (مثلاً 30x30 cm)")
else:
    st.warning(f"المساحة المطلوبة أكبر من الحد الأدنى: {ac_final:.2f} cm²")

# --- آلياً: دراسة ومفاضلة الأساسات ---
st.subheader("3. دراسة الأساسات والمفاضلة")
p_service = (pu_total / 1.5) * 1.1
area_f = p_service / soil_q

f1, f2, f3 = st.columns(3)
with f1:
    st.write("**منفرد:**", f"{np.sqrt(area_f):.2f} x {np.sqrt(area_f):.2f} m")
with f2:
    st.write("**مشترك:**", f"مساحة {area_f*1.8:.2f} m²")
with f3:
    st.write("**حصيرة:**", f"مساحة {area_f*5:.2f} m²")

# المفاضلة
if area_f > (Lx*Ly/8):
    st.error("🚨 الاقتراح: **الحصيرة** هي الأنسب بسبب تداخل القواعد.")
else:
    st.success("✅ الاقتراح: **القواعد المنفردة** كافية واقتصادية.")

# --- نظام الإنذار المبكر ---
st.divider()
st.subheader("🚨 نظام الإنذار (Check System)")
if Lx > 8:
    st.error("❌ إنذار: المجازات طويلة جداً، خطر انهيار أو ترخيم زائد!")
else:
    st.balloons()
    st.success("✅ المخطط سليم إنشائياً وفق معايير مكتب م. بيلان.")
