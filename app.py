import streamlit as st

def design_beam_syrian_code(fc, fy, b, d, Mu):
    # fc: مقاومة البيتون (MPa), fy: إجهاد الخضوع للحديد (MPa)
    # b, d: الأبعاد (mm), Mu: العزم التصميمي (kN.m)
    
    # تحويل الوحدات لـ N و mm
    Mu_nmm = Mu * 10**6
    
    # حساب قيمة Rn (معامل المقاومة)
    # معامل الأمان للبيتون (0.65 حسب الكود السوري في بعض الحالات أو حسب الطريقة)
    phi = 0.9 # معامل تخفيض المقاومة للعطف
    Rn = Mu_nmm / (phi * b * d**2)
    
    # حساب نسبة التسليح المطلوبة (rho)
    m = fy / (0.85 * fc)
    rho = (1 / m) * (1 - (1 - (2 * m * Rn / fy))**0.5)
    
    # مساحة التسليح المطلوبة
    As = rho * b * d
    
    return round(As, 2)

st.title("Pelan Syrian Code Master 🇸🇾")
st.subheader("تصميم الجوائز البيتونية - النسخة المتكاملة")

# مدخلات المستخدم
with st.sidebar:
    st.header("المعطيات الفنية")
    fc = st.number_input("إجهاد البيتون (fc') MPa", value=20)
    fy = st.number_input("إجهاد الحديد (fy) MPa", value=400)
    b = st.number_input("عرض الجائز (b) mm", value=200)
    h = st.number_input("الارتفاع الكلي (h) mm", value=500)
    cover = st.number_input("التغطية (mm)", value=40)
    Mu = st.number_input("العزم التصميمي (Mu) kN.m", value=150)

d = h - cover
As_required = design_beam_syrian_code(fc, fy, b, d, Mu)

st.success(f"مساحة التسليح المطلوبة: {As_required} mm²")

# زر لتصدير البيانات للـ VBA
if st.button("تصدير البيانات لجدول الكميات"):
    data = f"Beam;{b};{h};{As_required}"
    st.download_button("تحميل ملف الربط", data, file_name="design_output.csv")
