import streamlit as st

# --- 1. إعدادات الصفحة والختم ---
st.set_page_config(page_title="Petan Structural Pro", layout="wide")

# [cite: 2026-02-18]
eng_name = "المهندس المدني بيلان مصطفى عبدالكريم (Pelan)"
phone = "0998449697" # [cite: 2026-02-15]

# --- 2. قسم المدخلات (Input Section) ---
st.sidebar.header("📋 مدخلات التصميم")
width = st.sidebar.number_input("عرض الجائز (mm)", value=250)
depth = st.sidebar.number_input("ارتفاع الجائز (mm)", value=500)
moment = st.sidebar.number_input("العزم التصميمي Mu (kN.m)", value=150.0)
fy = st.sidebar.selectbox("إجهاد خضوع الحديد Fy", [400, 420, 500])

# --- 3. العمليات الحسابية ---
# حساب تقريبي للمساحة المطلوبة
d_eff = depth - 50
as_req = (moment * 10**6) / (0.9 * fy * 0.9 * d_eff)
num_bars = int(as_req / 201) + 1  # افتراض قطر 16

# --- 4. عرض المخطط (الرسم التخطيطي للحديد) ---
st.title("🏗️ Petan Structural Analysis Pro")
st.subheader("تفريد الحديد (Longitudinal Section)")

# رسم بسيط يمثل الجائز والحديد (بناءً على صورتك الأولى)
st.markdown(f"""
<div style="position: relative; width: 100%; height: 100px; background-color: #1a1a1a; border: 2px solid #555; margin-bottom: 20px;">
    <div style="position: absolute; top: 15px; left: 5%; right: 5%; height: 4px; background-color: #2196F3;"></div>
    <div style="position: absolute; top: 25px; left: 40%; color: #2196F3; font-weight: bold;">{num_bars} T 16 (Main Top)</div>
    
    <div style="display: flex; justify-content: space-around; width: 100%; height: 100%; align-items: center;">
        {"<div style='width: 1px; height: 70px; background-color: #d32f2f; opacity: 0.5;'></div>" * 15}
    </div>
</div>
""", unsafe_allow_html=True)

# --- 5. المخرجات والختم ---
col1, col2 = st.columns(2)
with col1:
    st.success(f"✅ المساحة المطلوبة: {as_req:.2f} mm²")
with col2:
    if num_bars > 8:
        st.error(f"⚠️ العدد مبالغ فيه: {num_bars} أسياخ")
    else:
        st.info(f"🔹 التسليح: {num_bars} T 16")

if num_bars > 8:
    st.warning("💡 نصيحة المهندس بيلان: يرجى زيادة عمق المقطع لتوفير الحديد.")

st.divider()
st.write(f"### {eng_name}")
st.write("دراسات - اشراف - تعهدات")
st.write(f"📞 هاتف: {phone}")
