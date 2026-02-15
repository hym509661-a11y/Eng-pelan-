import streamlit as st
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

# إعدادات الصفحة
st.set_page_config(page_title="المصمم الإنشائي - توقيع مباشر", layout="wide")

st.title("🏗️ نظام توقيع الأعمدة والجوائز بنقرة الفأرة")
st.write("ارفع المخطط المعماري (JPG/PNG) ثم انقر في أي مكان لوضع العنصر.")

# إدارة مخزن العناصر
if 'struct_data' not in st.session_state:
    st.session_state.struct_data = []

# القائمة الجانبية
with st.sidebar:
    st.header("🖼️ المخطط المعماري")
    bg_file = st.file_uploader("تحميل المخطط المعماري كخلفية", type=['png', 'jpg', 'jpeg'])
    
    st.divider()
    st.header("🛠️ اختيار العنصر")
    tool = st.radio("نوع العنصر الحالي:", ["عمود (Column)", "جائز (Beam)", "بلاطة هوردي", "بلاطة مصمتة"])
    b_val = st.number_input("العرض b (cm)", 30)
    h_val = st.number_input("الارتفاع/السمك h (cm)", 60)
    
    if st.button("🔴 مسح كل ما تم رسمه"):
        st.session_state.struct_data = []
        st.rerun()

# منطقة الرسم
if bg_file:
    original_img = Image.open(bg_file)
    # رسم العناصر القديمة فوق الصورة لعرضها باستمرار
    temp_img = original_img.copy()
    draw = ImageDraw.Draw(temp_img)
    
    for el in st.session_state.struct_data:
        x, y = el["x"], el["y"]
        # لون أحمر إذا كان العمود مخالف (مساحة < 900)
        color = "red" if el["type"] == "عمود (Column)" and el["area"] < 900 else "green"
        
        if "عمود" in el["type"]:
            draw.rectangle([x-10, y-10, x+10, y+10], fill=color, outline="black")
        elif "جائز" in el["type"]:
            draw.line([x, y, x+50, y], fill="blue", width=5)

    # الميزة الأهم: التقاط النقرة
    coords = streamlit_image_coordinates(temp_img, key="pill")

    if coords:
        new_x, new_y = coords["x"], coords["y"]
        area_calc = b_val * h_val
        
        # حفظ العنصر الجديد مكان النقرة
        st.session_state.struct_data.append({
            "type": tool,
            "x": new_x,
            "y": new_y,
            "b": b_val,
            "h": h_val,
            "area": area_calc
        })
        st.rerun() # تحديث الشاشة لإظهار العنصر الجديد فوراً

else:
    st.info("👈 يرجى تحميل المخطط المعماري من القائمة الجانبية للبدء بالرسم.")

# المذكرة الحسابية
if st.session_state.struct_data:
    st.divider()
    st.subheader("📋 المذكرة الحسابية والكميات")
    df = pd.DataFrame(st.session_state.struct_data)
    st.dataframe(df[["type", "b", "h", "area"]])
    
    # رسالة الإنذار
    for _, row in df.iterrows():
        if row['type'] == "عمود (Column)" and row['area'] < 900:
            st.error(f"🚨 تنبيه: يوجد عمود بمساحة {row['area']}cm² وهو مخالف للكود السوري!")
