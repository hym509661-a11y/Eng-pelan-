import streamlit as st
import math

st.set_page_config(page_title="المصمم الإنشائي الخاص", layout="centered")
st.title("🏗️ تطبيق المهندس الشخصي")

# قائمة العناصر
element = st.selectbox("اختر العنصر الإنشائي:", ["أعمدة محورية", "جوائز بيتونية", "بلاطات مصمتة", "أساسات منفردة"])

# مدخلات عامة
st.sidebar.header("إعدادات الكود السوري")
fcu = st.sidebar.number_input("fcu (MPa)", value=25)
fy = st.sidebar.number_input("fy (MPa)", value=400)
bar_dia = st.sidebar.selectbox("قطر الحديد (mm)", [12, 14, 16, 18, 20, 25])

if element == "أعمدة محورية":
    Pu = st.number_input("الحمل المصعد Pu (Ton)", value=150.0)
    b = st.number_input("العرض b (cm)", value=30)
    h = st.number_input("الارتفاع h (cm)", value=60)
    if st.button("حساب التسليح"):
        Ag = b * h * 100
        As = (Pu * 10000 - 0.35 * fcu * Ag) / (0.67 * fy - 0.35 * fcu)
        As_final = max(As, 0.008 * Ag)
        num = math.ceil(As_final / ((math.pi * bar_dia**2)/4))
        st.success(f"النتيجة: {num if num%2==0 else num+1} T{bar_dia}")

elif element == "جوائز بيتونية":
    Mu = st.number_input("العزم المصعد Mu (Ton.m)", value=15.0)
    b = st.number_input("العرض b (cm)", value=25)
    h = st.number_input("الارتفاع h (cm)", value=50)
    if st.button("حساب"):
        d = (h - 4) * 10
        Rn = (Mu * 10**7) / (b * 10 * d**2)
        m = fy / (0.85 * fcu)
        rho = (1/m) * (1 - math.sqrt(max(0, 1 - (2 * m * Rn / fy))))
        As = rho * (b * 10) * d
        num = math.ceil(As / ((math.pi * bar_dia**2)/4))
        st.success(f"التسليح السفلي: {num} T{bar_dia}")

st.info("هذا التطبيق مخصص للاستخدام الشخصي فقط.")
