import streamlit as st
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المصمم الإنشائي التفاعلي", layout="wide")

st.title("🏗️ توقيع العناصر الإنشائية بالنقر المباشر (الكود السوري)")
st.info("قم برفع المخطط المعماري، ثم انقر بالفأرة لتحديد مكان العمود أو الجائز.")

# --- إدارة البيانات (تخزين أماكن العناصر) ---
if 'elements' not in st.session_state:
    st.session_state.elements = []

# --- القائمة الجانبية ---
with st.sidebar:
    st.header("🖼️ إدارة المخطط")
    uploaded_bg = st.file_uploader("ارفع المخطط المعماري (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    
    st.divider()
    st.header("🛠️ أدوات الرسم")
    tool = st.radio("العنصر:", ["عمود (Column)", "جائز (Beam)", "بلاطة هوردي"])
    b_cm = st.number_input("العرض b (cm)", 30)
    h_cm = st.number_input("الارتفاع h (cm)", 60)
    
    if st.button("🧹 مسح المخطط والبدء من جديد"):
        st.session_state.elements = []
        st.rerun()

# --- منطقة العمل الرئيسية ---
if uploaded_bg:
    img = Image.open(uploaded_bg)
    # رسم العناصر المخزنة فوق الصورة قبل عرضها
    draw = ImageDraw.Draw(img)
    
    for el in st.session_state.elements:
        x, y = el["x"], el["y"]
        # تحديد لون الرسم (أحمر إذا كان العمود مخالف للكود < 900)
        color = "red" if el["area"] < 900 and el["type"] == "عمود (Column)" else "green"
        
        if "عمود" in el["type"]:
            # رسم مستطيل يمثل العمود مكان النقرة
            draw.rectangle([x-15, y-15, x+15, y+15], fill=color, outline="white")
        elif "جائز" in el["type"]:
            draw.line([x, y, x+100, y], fill="cyan", width=10)

    # عرض الصورة والتقاط إحداثيات النقرة الجديدة بالفأرة
    value = streamlit_image_coordinates(img, key="coords")

    if value:
        new_x, new_y = value["x"], value["y"]
        area = b_cm * h_cm
        
        # إضافة العنصر الجديد بناءً على مكان النقرة
        st.session_state.elements.append({
            "type": tool,
            "x": new_x,
            "y": new_y,
            "area": area,
            "b": b_cm,
            "h": h_cm
        })
        
        # إظهار تنذير فوري إذا كان العمود مخالف
        if tool == "عمود (Column)" and area < 900:
            st.warning(f"🚨 تنبيه: العمود الموقّع مساحته {area}cm² (أقل من 900cm²)")
        
        st.rerun() # لإعادة الرسم فوراً بعد النقرة

else:
    st.warning("👈 يرجى رفع صورة المخطط المعماري من القائمة الجانبية للبدء.")

# --- عرض البيانات والمذكرة ---
st.divider()
if st.session_state.elements:
    st.subheader("📑 قائمة العناصر الموقعة والمذكرة الحسابية")
    df = pd.DataFrame(st.session_state.elements)
    st.table(df[["type", "b", "h", "area"]])
    
    # ترويسة المذكرة
    st.write("### 📝 المذكرة الحسابية التلقائية")
    st.write(f"تم توقيع {len(df)} عناصر إنشائية وفق أبعاد الكود السوري (fcu=250, fy=4000).")
