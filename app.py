import streamlit as st
import numpy as np
import plotly.graph_objects as go

# إعداد الصفحة الاحترافي
st.set_page_config(page_title="المنظومة الإنشائية - م. بيلان", layout="wide")

# الختم الرسمي في أعلى البرنامج
st.markdown(f"""
    <div style="direction: rtl; text-align: right; border: 3px solid #2e7d32; padding: 15px; border-radius: 15px; background-color: #f1f8e9;">
        <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسية المتكاملة للتصميم الإنشائي</h1>
        <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
        <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>هاتف: 0998449697</b></p>
    </div>
""", unsafe_allow_html=True)

st.divider()

# القائمة الجانبية للمواد (كافة أنواع الحديد والبيتون)
st.sidebar.header("🛠️ مواصفات المواد (المواد)")
fcu = st.sidebar.select_slider("مقاومة الخرسانة fcu (MPa)", options=[20, 25, 30, 35, 40], value=25)
fy = st.sidebar.selectbox("إجهاد خضوع الحديد fy (MPa)", options=[240, 360, 400], index=2, help="240 للحديد الأملس، 400 للمجدول عالي المقاومة")
f_prime_c = 0.8 * fcu # تحويل الكود السوري

# اختيار العنصر الإنشائي
choice = st.sidebar.radio("اختر العنصر للتصميم:", ["البلاطات المسمطة", "الجوائز (Beams)", "الأعمدة", "الأساسات المنفردة"])

# --- 1. تصميم البلاطات والجوائز مع الرسم الدقيق ---
if choice in ["البلاطات المسمطة", "الجوائز (Beams)"]:
    st.header(f"💠 تصميم {choice}")
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        L = st.number_input("طول المجاز الفعال (m)", value=4.5)
        b = st.number_input("عرض المقطع b (mm)", value=1000 if choice == "البلاطات المسمطة" else 300)
        h = st.number_input("الارتفاع الكلي h (mm)", value=150 if choice == "البلاطات المسمطة" else 500)
        
        # أحمال المهندس بيلان
        st.subheader("📥 الأحمال")
        dl = st.number_input("الحمولة الميتة (kN/m² or kN/m)", value=2.5)
        ll = st.number_input("الحمولة الحية (kN/m² or kN/m)", value=3.0 if choice == "البلاطات المسمطة" else 10.0)
        
        wu = (1.4 * dl) + (1.7 * ll)
        mu = (wu * L**2) / 8 # عزم بسيط (بفرض الحالة الأسوأ)
        d = h - 25 # الارتفاع الفعال
        
    with col2:
        # محرك التصميم وفق جامعة دمشق
        rn = (mu * 1e6) / (0.9 * b * d**2)
        m = fy / (0.85 * f_prime_c)
        rho = (1/m) * (1 - np.sqrt(max(0, 1 - (2*m*rn/fy))))
        as_req = rho * b * d
        as_min = max(0.25 * np.sqrt(f_prime_c) / fy * b * d, 1.4 / fy * b * d)
        as_final = max(as_req, as_min)
        
        st.subheader("📊 النتائج الإنشائية")
        st.success(f"التسليح السفلي المطلوب: {as_final:.2f} mm²")
        
        # اختيار الأقطار
        dia = st.selectbox("اختر قطر القضيب (mm)", [8, 10, 12, 14, 16, 18, 20])
        n_bars = np.ceil(as_final / (np.pi * dia**2 / 4))
        st.info(f"النتيجة: **{int(n_bars)} T{dia}** {'لكل متر' if choice == 'البلاطات المسمطة' else 'للمقطع'}")

        # الرسم التوضيحي الدقيق (Section Sketch)
        fig = go.Figure()
        fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=3), fillcolor="rgba(128,128,128,0.2)")
        # رسم التسليح السفلي
        for i in range(int(n_bars)):
            x_pos = (b / (n_bars + 1)) * (i + 1)
            fig.add_shape(type="circle", x0=x_pos-dia/2, y0=20, x1=x_pos+dia/2, y1=20+dia, fillcolor="red", line_color="black")
        
        fig.update_layout(title="الرسم التوضيحي لمقطع العنصر والتسليح", xaxis_visible=False, yaxis_visible=False, height=300, width=500)
        st.plotly_chart(fig)

# --- 2. تصميم الأعمدة ---
elif choice == "الأعمدة":
    st.header("🏛️ تصميم الأعمدة المركزية")
    pu = st.number_input("الحمولة التصعيدية Pu (kN)", value=2000)
    col_b = st.number_input("عرض العمود B (mm)", value=300)
    col_h = st.number_input("عمق العمود H (mm)", value=500)
    
    ag = col_b * col_h
    # نسبة 1% حديد - اقتصادية الكود السوري
    ast_min = 0.01 * ag
    pn_max = 0.65 * 0.8 * (0.85 * f_prime_c * (ag - ast_min) + fy * ast_min) / 1000
    
    if pu > pn_max:
        st.error(f"❌ المقطع يحتاج لزيادة أبعاد أو تسليح إضافي. القدرة الحالية: {pn_max:.2f} kN")
    else:
        st.success(f"✅ المقطع آمن واقتصادي. التسليح الكلي: {ast_min:.2f} mm²")
        st.info(f"الاقتراح: {int(np.ceil(ast_min/201))} T16 قضبان طولية")

# --- 3. تصميم الأساسات ---
elif choice == "الأساسات المنفردة":
    st.header("🧱 تصميم الأساسات المنفردة")
    p_service = st.number_input("الحمولة التشغيلية P (kN)", value=1200)
    q_allow = st.number_input("تحمل التربة q (kN/m²)", value=150)
    
    area = (p_service * 1.1) / q_allow
    side = np.sqrt(area)
    st.success(f"أبعاد الأساس المقترحة: {side:.2f} x {side:.2f} m")
    st.caption("تم حساب الأبعاد مع اعتبار وزن الردم والوزن الذاتي للأساس.")

st.divider()
st.write(f"©️ تم التطوير بواسطة: {st.session_state.get('name', 'المهندس بيلان مصطفى عبدالكريم')}")
