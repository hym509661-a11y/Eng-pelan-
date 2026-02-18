import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="مكتب المهندس بيلان عبدالكريم", layout="centered")

# الختم الهندسي المعتمد
st.markdown(f"""
<div style="direction: rtl; text-align: right; border: 2px solid #2c3e50; padding: 15px; border-radius: 10px; background-color: #f8f9fa;">
    <h2 style="color: #2c3e50; margin: 0;">المهندس المدني: بيلان مصطفى عبدالكريم</h2>
    <p style="margin: 5px 0;"><b>دراسات - إشراف - تعهدات</b></p>
    <p style="color: #e74c3c; margin: 0;">هاتف: 0998449697</p>
</div>
""", unsafe_allow_stdio=True)

st.title("🏗️ نظام الدراسة الإنشائية المتكامل")
st.write("وفق الكود العربي السوري لعام 2012")

# تبويبات العناصر الإنشائية
tab1, tab2, tab3 = st.tabs(["تصميم الجوائز", "تصميم الأعمدة", "الزلازل والقواعد"])

with tab1:
    st.header("تصميم المقاطع المستطيلة")
    col1, col2 = st.columns(2)
    with col1:
        mu = st.number_input("العزم التصميمي (Mu) طن.متر", value=10.0)
        b = st.number_input("عرض المقطع (b) سم", value=20.0)
    with col2:
        d = st.number_input("الارتفاع الفعال (d) سم", value=55.0)
        fpc = st.number_input("المقاومة (f'c) كغ/سم2", value=200)

    if st.button("احسب تسليح الجائز"):
        Mu_kgcm = mu * 10**5
        phi = 0.9
        fy = 3600
        rn = Mu_kgcm / (phi * b * d**2)
        
        try:
            rho = (0.85 * fpc / fy) * (1 - math.sqrt(1 - (2.353 * rn / fpc)))
            rho_min = max(14/fy, (0.25 * math.sqrt(fpc))/fy)
            rho = max(rho, rho_min)
            as_req = rho * b * d
            
            # اختيار الأقطار
            bars_14 = math.ceil(as_req / 1.54)
            bars_16 = math.ceil(as_req / 2.01)
            
            st.success(f"مساحة الحديد المطلوبة: {as_req:.2f} سم2")
            st.info(f"خيارات التسليح: {bars_14} T 14 أو {bars_16} T 16")
        except:
            st.error("المقطع صغير جداً بالنسبة للعزم المطبق!")

with tab2:
    st.header("تصميم الأعمدة الطويلة والقصير")
    pu = st.number_input("الحمولة التصميمية (Pu) طن", value=120.0)
    col_b = st.number_input("عرض العمود (b) سم", value=30.0)
    col_h = st.number_input("عمق العمود (h) سم", value=50.0)
    
    if st.button("احسب تسليح العمود"):
        pu_kg = pu * 1000
        ag = col_b * col_h
        phi = 0.65
        ast = (pu_kg / (0.8 * phi) - 0.85 * fpc * ag) / (3600 - 0.85 * fpc)
        ast = max(ast, 0.01 * ag)
        
        bars_16 = math.ceil(ast / 2.01)
        if bars_16 % 2 != 0: bars_16 += 1
        
        st.success(f"مساحة الحديد المطلوبة: {ast:.2f} سم2")
        st.info(f"التسليح المقترح: {bars_16} T 16 موزعة بانتظام")

with tab3:
    st.header("الزلازل والقواعد")
    st.info("سيتم إضافة موديول توزيع القوى الزلزالية وحساب القواعد المشتركة في التحديث القادم.")

st.markdown("---")
st.caption("تم تطوير النظام بواسطة المهندس بيلان عبدالكريم - 2026")
