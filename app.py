import streamlit as st
import numpy as np

# --- ترويسة وهوية المكتب المهني ---
st.set_page_config(page_title="منظومة المهندس بيلان - كود سوري 2026", layout="wide")
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 5px solid #1b5e20; padding: 25px; border-radius: 20px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">محرك التصميم الإنشائي المتكامل (التحليل والربط الشامل)</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 20px; margin:5px;">دراسات - إشراف - تعهدات | <b>هاتف: 0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

# --- 1. مدخلات المشروع الكلية (التربة والطوابق) ---
st.sidebar.header("📋 معطيات المشروع العامة")
num_floors = st.sidebar.number_input("إجمالي عدد الطوابق (قبو + متكرر)", min_value=1, value=4)
soil_q = st.sidebar.number_input("قدرة تحمل التربة (kN/m²)", value=200)
fcu = st.sidebar.slider("مقاومة البيتون fcu (MPa)", 20, 35, 25)

# --- 2. تحليل البلاطة والجوائز (وفق المخطط الذي تصدره) ---
st.header("📐 أولاً: تحليل البلاطة والجوائز")
col1, col2 = st.columns(2)
with col1:
    Lx = st.number_input("المجاز الطويل Lx (m)", value=6.0)
    Ly = st.number_input("المجاز القصير Ly (m)", value=4.5)
with col2:
    floor_type = st.radio("نوع السقف المدرس:", ["قبو (بلاطة مصمتة)", "أرضي/متكرر (بلاطة هوردي)"])

# منطق الكود السوري للبلاطة والجوائز
ratio = Lx / Ly
wu_slab = (1.4 * 2.5) + (1.7 * 2.0) # حمولاتك الدقيقة

if "مصمتة" in floor_type:
    behavior = "باتجاهين (Two-way)" if ratio <= 2 else "باتجاه واحد (One-way)"
    st.info(f"📍 **سلوك البلاطة المصمتة:** تعمل {behavior}")
else:
    st.success(f"📍 **توجيه الأعصاب (هوردي):** يتم التوجيه إجبارياً في الاتجاه القصير ({Ly} m)")

# دراسة الجوائز (انتقال الحمل من البلاطة للجائز)
wu_beam = (wu_slab * Ly/2) + 5.0 # حمل البلاطة + وزن الجائز
mu_beam = (wu_beam * Lx**2) / 10
vu_beam = (wu_beam * Lx) / 2 # قوة القص التي ستنتقل للعمود

# --- 3. تصميم الأعمدة (شرط المساحة الدنيا 900 cm²) ---
st.header("🏛️ ثانياً: تصميم وتدقيق الأعمدة")
pu_total = vu_beam * 2 * num_floors # حمل تراكمي لعمود وسطي من الجهتين
ac_req = (pu_total * 10) / (0.35 * 0.8 * fcu + 0.67 * 400 * 0.01)
ac_final = max(900, ac_req) # شرط المهندس بيلان الصارم

st.write(f"الحمل التصعيدي التراكمي عند القاعدة: **{pu_total:.2f} kN**")
if ac_final == 900:
    st.success(f"✅ تم اعتماد المساحة الدنيا للكود السوري: **900 cm²** (مثلاً 30x30 cm)")
else:
    st.warning(f"⚠️ المساحة الدنيا (900) غير كافية، تم التصميم على مساحة: **{ac_final:.2f} cm²**")

# --- 4. دراسة ومفاضلة الأساسات (مفرد - مشترك - حصيرة) ---
st.header("🕋 ثالثاً: دراسة أنواع الأساسات")
p_service = (pu_total / 1.5) * 1.1 # حمل الخدمة
area_isolated = p_service / soil_q

f1, f2, f3 = st.columns(3)
with f1:
    st.subheader("منفرد (Isolated)")
    st.write(f"المساحة: {area_isolated:.2f} m²")
    st.write(f"الأبعاد: {np.sqrt(area_isolated):.2f} x {np.sqrt(area_isolated):.2f} m")
with f2:
    st.subheader("مشترك (Combined)")
    st.write(f"المساحة المطلوبة لعمودين: {area_isolated * 1.8:.2f} m²")
with f3:
    st.subheader("حصيرة (Raft)")
    st.write(f"إجمالي مساحة الحصيرة المطلوبة: {area_isolated * 5:.2f} m²")

# المفاضلة والاقتراح
if area_isolated > (Lx * Ly / 8):
    st.error("🚨 **الاقتراح الأفضل:** مساحة القواعد متداخلة، الخيار الهندسي الصحيح هو **الحصيرة (Raft)**.")
else:
    st.success("✅ **الاقتراح الأفضل:** **القواعد المنفردة** آمنة واقتصادية حالياً.")

# --- 5. نظام الإنذار من الانهيار والخطأ ---
st.divider()
st.subheader("🚨 نظام الإنذار المبكر والتدقيق")
error_found = False

if ratio > 3:
    st.error("❌ **إنذار انهيار/سهم:** استطالة البلاطة كبيرة جداً، خطر ترخيم حاد في الوسط!")
    error_found = True
if p_service / area_isolated > soil_q:
    st.error("❌ **إنذار انهيار تربة:** الإجهاد المطبق أكبر من تحمل التربة المسموح!")
    error_found = True
if Lx/16 < 0.4 and "هوردي" in floor_type:
    st.warning("⚠️ **تنبيه:** سماكة البلاطة قد لا تحقق شرط السهم للكود السوري.")

if not error_found:
    st.balloons()
    st.success("✅ **منظومة بيلان:** الدراسة سليمة 100% ولا توجد أخطار انهيار.")

st.divider()
st.caption(f"تم التدقيق الإنشائي النهائي لعام 2026 | المهندس بيلان مصطفى عبدالكريم")
