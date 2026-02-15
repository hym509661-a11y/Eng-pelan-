import streamlit as st
import pandas as pd
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ملاحظة: تم استبدال ezdxf بمحاكي في حال عدم توفر المكتبة لضمان عمل التطبيق
try:
    import ezdxf
except ImportError:
    ezdxf = None

st.set_page_config(page_title="المهندس AI - التصميم التفاعلي", layout="wide")

# --- إدارة البيانات ---
if 'elements' not in st.session_state:
    st.session_state.elements = []

# --- واجهة رفع الملف ---
st.title("🏗️ منصة التوقيع الإنشائي الذكية")
uploaded_file = st.file_uploader("📂 ارفع المخطط المعماري (DXF)", type=['dxf'])

# --- القائمة الجانبية لإضافة العناصر ---
with st.sidebar:
    st.header("🛠️ إضافة عناصر إنشائية")
    el_type = st.radio("نوع العنصر", ["عمود (Column)", "جائز (Beam)"])
    
    col1, col2 = st.columns(2)
    with col1:
        x_pos = st.number_input("موقع X (m)", 0.0, 20.0, 2.0, step=0.1)
        width = st.number_input("العرض b (cm)", 20, 100, 30)
    with col2:
        y_pos = st.number_input("موقع Y (m)", 0.0, 20.0, 2.0, step=0.1)
        depth = st.number_input("الارتفاع/العمق h (cm)", 20, 150, 60)
    
    rebar = st.selectbox("قطر التسليح (mm)", [12, 14, 16, 18, 20, 25])

    if st.button("➕ إضافة العنصر للوحة"):
        st.session_state.elements.append({
            "type": el_type, "x": x_pos, "y": y_pos, 
            "b": width, "h": depth, "rebar": rebar
        })
    
    if st.button("🧹 مسح اللوحة"):
        st.session_state.elements = []

# --- عرض اللوحة والمذكرة ---
c_draw, c_memo = st.columns([2, 1])

with c_draw:
    st.subheader("📍 لوحة التوقيع (Layout)")
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_facecolor('#f0f2f6')
    
    # رسم المخطط المعماري كخلفية (Simulation)
    if uploaded_file:
        ax.text(5, 5, "Architectural Layer Active", alpha=0.2, fontsize=20, ha='center')
        
    # رسم العناصر الموقعة
    for el in st.session_state.elements:
        if "Column" in el["type"]:
            # رسم العمود بمقاسه الحقيقي (تحويل سم لـ متر)
            rect = patches.Rectangle(
                (el["x"] - el["b"]/200, el["y"] - el["h"]/200), 
                el["b"]/100, el["h"]/100, color='black', zorder=10
            )
            ax.add_patch(rect)
            ax.text(el["x"], el["y"]+0.3, f"C {el['b']}x{el['h']}", fontsize=8, ha='center')
        else:
            # رسم الجائز (بافتراض طول افتراضي 4 متر للتوضيح)
            ax.plot([el["x"], el["x"]+4], [el["y"], el["y"]], color='#1f77b4', lw=el["b"]/10, alpha=0.8)
            ax.text(el["x"]+2, el["y"]+0.1, f"B {el['b']}x{el['h']}", fontsize=8, color='#1f77b4')

    ax.set_xlim(0, 15); ax.set_ylim(0, 15)
    ax.grid(True, linestyle='--', alpha=0.5)
    st.pyplot(fig)

with c_memo:
    st.subheader("📑 المذكرة الحسابية الحية")
    if st.session_state.elements:
        # حساب أطول بحر بين العناصر الموقعة
        spans = [4.0] # قيمة افتراضية
        L = max(spans)
        
        st.write("### تصميم البلاطة")
        t_hordy = math.ceil((L * 100) / 21)
        st.latex(r"t = \frac{L}{21} = " + str(t_hordy) + r"\text{ cm}")
        
        st.write("### جدول الكميات المخصص")
        df = pd.DataFrame(st.session_state.elements)
        st.table(df[["type", "b", "h", "rebar"]])
    else:
        st.info("قم بإضافة أعمدة وجوائز لبدء الحسابات.")

# --- الصور التوضيحية ---
st.divider()
st.header("🔍 التفاصيل الإنشائية الناتجة")
col_img1, col_img2 = st.columns(2)

with col_img1:
        st.caption("تفصيلة تسليح الأعمدة الموقعة")

with col_img2:
        st.caption("تفصيلة بلاطة الهوردي والسماكة المحسوبة")
