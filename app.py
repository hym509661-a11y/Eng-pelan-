import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي التفاعلي", layout="wide")

st.title("🏗️ نظام توقيع العناصر الإنشائية فوق المخطط المعماري")

# --- إدارة البيانات (تخزين أماكن الأعمدة والجوائز) ---
if 'struct_elements' not in st.session_state:
    st.session_state.struct_elements = []

# --- القائمة الجانبية للأدوات ---
with st.sidebar:
    st.header("🖼️ المخطط المعماري")
    # زر رفع المخطط المعماري (المصدر من أوتوكاد كصورة أو PDF)
    uploaded_bg = st.file_uploader("ارفع صورة المخطط (JPG/PNG/PDF)", type=['png', 'jpg', 'jpeg'])
    
    st.divider()
    st.header("🛠️ أدوات التوقيع")
    tool = st.radio("العنصر المراد رسمه:", ["عمود (Column)", "جائز (Beam)", "بلاطة هوردي", "بلاطة مصمتة"])
    
    col1, col2 = st.columns(2)
    with col1: b_dim = st.number_input("العرض b (cm)", 30)
    with col2: h_dim = st.number_input("الارتفاع h (cm)", 60)
    
    if st.button("🧹 مسح جميع العناصر"):
        st.session_state.struct_elements = []

# --- منطقة الرسم التفاعلية ---
st.subheader("📍 انقر لتحديد أماكن العناصر (الإحداثيات)")

c_map, c_memo = st.columns([3, 1])

with c_map:
    # لتحديد المكان بدقة، نستخدم مدخلات رقمية أو خريطة تفاعلية
    # ملاحظة: في تطبيقات الويب نستخدم الإحداثيات لمحاكاة الفأرة
    col_x, col_y = st.columns(2)
    with col_x: x_click = st.number_input("إحداثي X (بالأمتار)", 0.0, 50.0, step=0.05)
    with col_y: y_click = st.number_input("إحداثي Y (بالأمتار)", 0.0, 50.0, step=0.05)
    
    if st.button("🎯 تثبيت العنصر في هذا الموقع"):
        # فحص كود الـ 900 سم مربع
        area = b_dim * h_dim
        status = "✅ مطابق"
        if tool == "عمود (Column)" and area < 900:
            st.error(f"⚠️ إنذار: المقطع {area}cm² أصغر من 900cm²")
            status = "🚨 إنذار (مساحة صغيرة)"
        
        st.session_state.struct_elements.append({
            "نوع": tool, "x": x_click, "y": y_click, "b": b_dim, "h": h_dim, "الحالة": status
        })

    # إنشاء لوحة الرسم
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # 1. إظهار المخطط المعماري كخلفية
    if uploaded_bg:
        img = Image.open(uploaded_bg)
        ax.imshow(img, extent=[0, 20, 0, 20], alpha=0.6) # تمثيل المخطط كخلفية شفافة قليلاً
    else:
        ax.set_facecolor('#242424') # خلفية سوداء في حال عدم وجود مخطط
        ax.text(10, 10, "يرجى رفع المخطط المعماري كخلفية", color='white', ha='center')

    # 2. رسم العناصر الإنشائية فوق الخلفية
    for el in st.session_state.struct_elements:
        b_m = el["b"]/100
        h_m = el["h"]/100
        if "عمود" in el["نوع"]:
            color = 'red' if "إنذار" in el["الحالة"] else '#00FF00'
            ax.add_patch(patches.Rectangle((el["x"]-b_m/2, el["y"]-h_m/2), b_m, h_m, color=color, zorder=5))
        elif "جائز" in el["نوع"]:
            ax.plot([el["x"], el["x"]+4], [el["y"], el["y"]], color='#00FFFF', lw=el["b"]/10, zorder=4)
        elif "هوردي" in el["نوع"]:
            ax.add_patch(patches.Rectangle((el["x"], el["y"]), 4, 3, hatch='///', edgecolor='yellow', fill=False, zorder=3))

    ax.set_xlim(0, 20); ax.set_ylim(0, 20)
    ax.grid(True, linestyle='--', alpha=0.3)
    st.pyplot(fig)

with c_memo:
    st.subheader("📑 المذكرة والكميات")
    st.write(f"**المهندس المصمم:** {st.session_state.get('eng_name', 'غير محدد')}")
    if st.session_state.struct_elements:
        df = pd.DataFrame(st.session_state.struct_elements)
        st.dataframe(df[["نوع", "b", "h", "الحالة"]])
        
        # حسابات الهوردي التلقائية
        st.divider()
        st.write("### حسابات البلاطة")
        st.latex(r"t = L_{max} / 21")
