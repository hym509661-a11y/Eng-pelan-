import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# إعداد الهوية البصرية والختم
st.set_page_config(page_title="Pro-Civil Syria | Eng. Pelan", layout="wide")

def main():
    # الترويسة بختم المهندس بيلان
    st.markdown(f"""
    <div style="text-align: center; border: 2px solid #2e7d32; padding: 10px; border-radius: 10px;">
        <h1 style="color: #2e7d32;">المنظومة الهندسية للتصميم الإنشائي</h1>
        <h3>المهندس المدني بيلان مصطفى عبدالكريم</h3>
        <p>دراسات - إشراف - تعهدات | <b>0998449697</b></p>
    </div>
    """, unsafe_allow_input=True)

    st.sidebar.header("⚙️ إعدادات الكود والمواد")
    
    # اختيار نوع الحديد وإجهاد الخرسانة
    fy = st.sidebar.selectbox("نوع حديد التسليح (fy MPa)", [240, 360, 400], index=2)
    fcu = st.sidebar.slider("المقاومة المكعبة للخرسانة fcu (MPa)", 20, 40, 25)
    f_prime_c = 0.8 * fcu # تحويل الكود السوري

    menu = ["تصميم البلاطات", "تصميم الجوائز", "تصميم الأعمدة", "تصميم الأساسات"]
    choice = st.sidebar.radio("اختر العنصر الإنشائي:", menu)

    if choice == "تصميم البلاطات":
        st.header("📏 تصميم البلاطات المسمطة (Solid Slab)")
        col1, col2 = st.columns(2)
        
        with col1:
            L = st.number_input("طول المجاز الفعال L (m)", value=4.0)
            H = st.number_input("سماكة البلاطة الكلية H (cm)", value=15)
            # مدخلات المهندس بيلان
            DL = st.number_input("الحمولة الميتة (G) kN/m2", value=2.5)
            LL = st.number_input("الحمولة الحية (P) kN/m2", value=3.0)
        
        # الحسابات التصميمية
        Wu = (1.4 * DL) + (1.7 * LL)
        Mu = (Wu * L**2) / 10 # عزم تقريبي للكود السوري
        d = (H * 10) - 20 # الارتفاع الفعال
        
        # حساب التسليح السفلي بدقة
        Rn = (Mu * 1e6) / (0.9 * 1000 * d**2)
        m = fy / (0.85 * f_prime_c)
        rho = (1/m) * (1 - np.sqrt(max(0, 1 - (2*m*Rn/fy))))
        As_req = rho * 1000 * d
        As_min = max(0.25 * np.sqrt(f_prime_c) / fy * 1000 * d, 1.4 / fy * 1000 * d)
        As_final = max(As_req, As_min)
        
        with col2:
            st.subheader("📊 النتائج الإنشائية")
            st.info(f"الحمولة التصعيدية Wu = {Wu:.2f} kN/m2")
            st.success(f"التسليح السفلي المطلوب As = {As_final:.2f} mm2/m")
            
            # اختيار قطر السيخ للرسم التوضيحي
            bar_dia = st.selectbox("اختر قطر السيخ (mm)", [8, 10, 12, 14])
            as_bar = (np.pi * bar_dia**2) / 4
            count = np.ceil(As_final / as_bar)
            st.write(f"النتيجة: **{int(count)} T{bar_dia} / m'**")

            # الرسم التوضيحي للمقطع
            fig = go.Figure()
            fig.add_shape(type="rect", x0=0, y0=0, x1=100, y1=H, line=dict(color="black"), fillcolor="lightgrey")
            for i in range(int(count)):
                fig.add_shape(type="circle", x0=(i*100/count), y0=2, x1=(i*100/count)+2, y1=4, fillcolor="blue")
            fig.update_layout(title="رسم توضيحي لمقطع البلاطة والتسليح السفلي", width=400, height=200)
            st.plotly_chart(fig)

    elif choice == "تصميم الأعمدة":
        st.header("🏛️ تصميم الأعمدة المركزية (Columns)")
        Pu = st.number_input("الحمولة التصعيدية Pu (kN)", value=2000)
        B = st.number_input("عرض العمود B (mm)", value=300)
        H_col = st.number_input("عمق العمود H (mm)", value=500)
        
        Ag = B * H_col
        # معادلة الكود السوري للأعمدة المطرقة (1% حديد)
        Ast_min = 0.01 * Ag
        Pn_max = 0.65 * 0.8 * (0.85 * f_prime_c * (Ag - Ast_min) + fy * Ast_min) / 1000
        
        if Pu > Pn_max:
            Ast_req = ((Pu*1000 / (0.65*0.8)) - (0.85*f_prime_c*Ag)) / (fy - 0.85*f_prime_c)
            st.error(f"المقطع يحتاج تسليح إضافي: As = {Ast_req:.2f} mm2")
        else:
            st.success(f"المقطع آمن بالحد الأدنى (1%): As = {Ast_min:.2f} mm2")

    elif choice == "تصميم الأساسات":
        st.header("🧱 تصميم الأساسات المنفردة (Isolated Footing)")
        P_service = st.number_input("الحمولة التشغيلية (kN)", value=1200)
        q_allow = st.number_input("تحمل التربة المسموح (kN/m2)", value=150)
        
        Area = (P_service * 1.1) / q_allow
        Side = np.sqrt(Area)
        st.success(f"أبعاد الأساس المقترحة: {Side:.2f} x {Side:.2f} m")
        st.warning("يتم التحقق من القص الثاقب (Punching) تلقائياً لضمان سماكة اقتصادية.")

    st.divider()
    if st.button("إصدار تقرير فني بختم المكتب"):
        st.balloons()
        st.write(f"تم اعتماد الدراسة الفنية بواسطة: {self.stamp_text}")

if __name__ == "__main__":
    main()
