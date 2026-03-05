import streamlit as st
import math

# إعدادات الصفحة
st.set_page_config(page_title="برج دمشق - م. بيلان", layout="wide")
st.sidebar.markdown("### 🏗️ المكتب الهندسي")
st.sidebar.info("المهندس بيلان مصطفى عبدالكريم\nمشروع برج سكني 11 طابق")

st.title("الحاسبة الإنشائية الديناميكية (الكود السوري)")
st.write("قم بتغيير طول المجاز، وستتغير القيم المعتمدة (بالأخضر) تلقائياً")

# المدخل الأساسي: طول المجاز
L = st.number_input("أدخل طول أكبر مجاز L (cm):", value=530, step=10)

st.markdown("---")
col1, col2 = st.columns(2)

# --- قسم الجوائز (Beams) ---
with col1:
    st.header("📏 الجوائز (Beams)")
    
    # 1. الجوائز الساقطة (حسب الملف: L/14 + 10cm أمان)
    h_drop_req = L / 14
    h_drop_final = math.ceil((h_drop_req + 10) / 5) * 5 # تقريب لأقرب 5 سم
    
    st.subheader("الجائز الساقط (سقف القبو)")
    st.write(f"المطلوب إنشائياً (L/14): {h_drop_req:.1f} cm")
    st.success(f"القيمة المعتمدة بالأخضر: 30 × {h_drop_final} cm")
    
    # 2. الجوائز المخفية (حسب الملف: وسطية L/4)
    b_hidden_req = L / 4
    b_hidden_final = max(105, math.ceil(b_hidden_req / 5) * 5)
    
    st.subheader("الجائز المخفي (الهوردي)")
    st.write(f"المطلوب للجائز الوسطي (L/4): {b_hidden_req:.1f} cm")
    st.success(f"القيمة المعتمدة بالأخضر: عرض {b_hidden_final} cm")

# --- قسم البلاطات والأساسات ---
with col2:
    st.header("🏗️ البلاطات والأساسات")
    
    # 1. بلاطة الهوردي (حسب حالة الاستمرار)
    st.subheader("بلاطة الهوردي")
    case = st.selectbox("حالة الاستمرار:", ["مستمرة طرفين (L/20)", "مستمرة طرف (L/18)", "بسيطة (L/16)"])
    divs = {"مستمرة طرفين (L/20)": 20, "مستمرة طرف (L/18)": 18, "بسيطة (L/16)": 16}
    
    h_rib_min = L / divs[case]
    h_rib_final = max(30, math.ceil(h_rib_min / 2) * 2) # الحد الأدنى بالمشروع 30 سم
    
    st.write(f"المطلوب إنشائياً: {h_rib_min:.1f} cm")
    st.success(f"القيمة المعتمدة بالأخضر: {h_rib_final} cm")
    
    # 2. الحصيرة (حسب الكود السوري L/6)
    st.subheader("الحصيرة (Raft)")
    h_raft_min = L / 6
    h_raft_final = max(90, math.ceil(h_raft_min / 10) * 10) # الحد الأدنى 90 سم
    
    st.write(f"المطلوب حسب الكود السوري (L/6): {h_raft_min:.1f} cm")
    st.success(f"القيمة المعتمدة بالأخضر: {h_raft_final} cm")

# --- قسم الدرج (حسب معطيات الملف) ---
st.markdown("---")
st.header("🪜 حسابات الدرج (الشاحط)")
L_stair = 290 # ثابت حسب ملفك
h_stair_final = max(15, math.ceil((L_stair/20)))

col_s1, col_s2 = st.columns(2)
col_s1.write(f"طول الشاحط: {L_stair} cm")
col_s1.success(f"سماكة الشاحط المعتمدة (L/20): {h_stair_final} cm")
col_s2.write("زاوية الميل: 27°")
col_s2.write("الحمولة الحية المعتمدة: 4 kN/m²")

st.divider()
st.caption("تمت البرمجة وفق دراسة الدكتور فادي نقرش - إعداد المهندس بيلان مصطفى")
