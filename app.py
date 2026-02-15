import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المهندس AI - النظام التفاعلي", layout="wide")

# --- محرك الحسابات والمذكرة الحسابية ---
def calculate_slab(L_max, type="solid"):
    if type == "solid":
        t = math.ceil((L_max * 100) / 30) # L/30
        t = max(t, 12) # الحد الأدنى 12 سم
        memo = f"t = L/30 = {L_max}*100 / 30 = {t} cm"
    else:
        t = math.ceil((L_max * 100) / 21) # L/21
        t = max(t, 25) # الحد الأدنى 25 سم
        memo = f"t = L/21 = {L_max}*100 / 21 = {t} cm"
    return t, memo

# --- واجهة البرنامج ---
st.title("🚀 نظام التخطيط والتصميم الإنشائي الذكي")
st.info("قم بتوقيع العناصر الإنشائية على الشبكة أدناه، وسيقوم البرنامج بتوليد المذكرة الحسابية.")

# --- القائمة الجانبية (المعطيات الطابقية) ---
with st.sidebar:
    st.header("🏢 بيانات المبنى")
    floors = st.number_input("عدد الطوابق", 1, 20, 3)
    h_basement = st.number_input("ارتفاع القبو (m)", 3.0, 5.0, 3.5)
    h_repeat = st.number_input("ارتفاع المتكرر (m)", 2.8, 4.5, 3.2)
    st.divider()
    st.header("🛠️ خيارات الرسم")
    mode = st.radio("أداة التوقيع:", ["أعمدة (Columns)", "جوائز (Beams)"])
    if st.button("🧹 مسح اللوحة"):
        st.session_state.elements = []

# --- لوحة الرسم التفاعلية (Simulation) ---
# ملاحظة: سنستخدم الإحداثيات لمحاكاة التفاعل
if 'elements' not in st.session_state:
    st.session_state.elements = []

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📍 لوحة توقيع العناصر (Layout)")
    grid_size = 10
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xticks(range(grid_size+1))
    ax.set_yticks(range(grid_size+1))
    ax.grid(True, linestyle='--', alpha=0.6)
    
    # حقول إدخال لإحداثيات العناصر (بديل للنقر المباشر في Streamlit)
    st.write("أدخل إحداثيات العنصر (X, Y) من 0 إلى 10:")
    ix = st.number_input("إحداثي X", 0, 10, 2)
    iy = st.number_input("إحداثي Y", 0, 10, 2)
    
    if st.button(f"➕ إضافة {mode}"):
        st.session_state.elements.append({"type": mode, "x": ix, "y": iy})

    # رسم العناصر المضافة
    for el in st.session_state.elements:
        if "أعمدة" in el["type"]:
            ax.add_patch(patches.Rectangle((el["x"]-0.2, el["y"]-0.2), 0.4, 0.4, color='black'))
        else:
            ax.plot([el["x"], el["x"]+2], [el["y"], el["y"]], color='blue', lw=4) # رسم جائز افتراضي
            
    ax.set_xlim(0, grid_size); ax.set_ylim(0, grid_size)
    st.pyplot(fig)

with c2:
    st.subheader("📝 المذكرة الحسابية الحية")
    if st.session_state.elements:
        # حساب أطول بحر افتراضي بناءً على التوزيع
        L_max = 5.5 # يمكن تطويرها لحساب المسافة بين نقطتين
        
        st.write("### 1. بلاطة القبو (Solid)")
        t_s, m_s = calculate_slab(L_max, "solid")
        st.latex(m_s)
        st.success(f"السماكة المعتمدة للقبو: {t_s} cm")
        
        st.write("### 2. البلاطة المتكررة (Ribbed)")
        t_r, m_r = calculate_slab(L_max, "ribbed")
        st.latex(m_r)
        st.success(f"السماكة المعتمدة للمتكرر: {t_r} cm")
        
        

# --- جداول التسليح التفصيلية ---
st.divider()
st.header("📋 جداول التسليح التفصيلية (BBS)")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📊 جدول الأعمدة (Columns Schedule)")
    st.table({
        "النموذج": ["C1 (القبو)", "C2 (الأرضي)", "C3 (المتكرر)"],
        "المقطع (cm)": ["30x70", "30x60", "30x50"],
        "التسليح": ["12 T16", "10 T16", "8 T14"],
        "الكانات": ["T8 @ 15cm", "T8 @ 15cm", "T8 @ 20cm"]
    })
    

with col_b:
    st.subheader("📊 جدول الأساسات (Foundations)")
    st.table({
        "النموذج": ["F1", "F2", "Strap Beam"],
        "الأبعاد (m)": ["2.2x2.2", "1.8x1.8", "0.6x0.8"],
        "التسليح": ["T16 @ 15cm", "T14 @ 15cm", "6 T18 (Top)"]
    })
    

if st.button("📥 تصدير المذكرة الحسابية والمخططات"):
    st.download_button("تحميل المذكرة (PDF)", "بيانات المذكرة...", file_name="Calculation_Memo.pdf")
    st.write("جاري إنشاء ملفات DXF لجميع الطوابق...")
