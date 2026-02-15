import streamlit as st
import pandas as pd
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw
import datetime

# إعدادات الواجهة
st.set_page_config(page_title="Syria-SAFE Cloud", layout="wide")

# إدارة البيانات
if 'struct_elements' not in st.session_state:
    st.session_state.struct_elements = []

# القائمة الجانبية
with st.sidebar:
    st.title("💠 Syria-SAFE v2")
    uploaded_bg = st.file_uploader("ارفع مخطط الأوتوكاد (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    
    st.divider()
    st.header("🔍 التحكم بالزوم")
    zoom = st.slider("مستوى التقريب", 1.0, 10.0, 1.0)
    
    st.divider()
    tool = st.selectbox("العنصر:", ["Column", "Beam", "Hordy"])
    b_val = st.number_input("العرض b (cm)", 30)
    h_val = st.number_input("الارتفاع h (cm)", 60)
    
    if st.button("🧹 مسح المخطط"):
        st.session_state.struct_elements = []
        st.rerun()

# منطقة العمل
if uploaded_bg:
    img = Image.open(uploaded_bg)
    w, h = img.size
    
    # حساب منطقة الزوم (وسط الصورة حالياً للتبسيط)
    view_w, view_h = w/zoom, h/zoom
    left, top = (w-view_w)/2, (h-view_h)/2
    view_img = img.crop((left, top, left+view_w, top+view_h))
    
    draw = ImageDraw.Draw(view_img)
    # رسم العناصر المخزنة
    for el in st.session_state.struct_elements:
        # تحويل الإحداثيات لتناسب الزوم
        rel_x = (el['x_abs'] - left) * (view_img.width / view_w)
        rel_y = (el['y_abs'] - top) * (view_img.height / view_h)
        if 0 <= rel_x <= view_img.width and 0 <= rel_y <= view_img.height:
            color = "red" if el['area'] < 900 and el['type']=="Column" else "green"
            draw.rectangle([rel_x-10, rel_y-10, rel_x+10, rel_y+10], fill=color, outline="white")

    # النقر المباشر
    coords = streamlit_image_coordinates(view_img, key="safe_v2")

    if coords:
        # تحويل النقرة لإحداثيات الصورة الأصلية
        abs_x = left + (coords['x'] * (view_w / view_img.width))
        abs_y = top + (coords['y'] * (view_h / view_img.height))
        
        area = b_val * h_val
        st.session_state.struct_elements.append({
            "type": tool, "x_abs": abs_x, "y_abs": abs_y, 
            "b": b_val, "h": h_val, "area": area
        })
        st.rerun()
else:
    st.info("💡 ارفع المخطط المعماري من القائمة الجانبية للبدء.")

# المذكرة والجداول
if st.session_state.struct_elements:
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 جداول العناصر")
        df = pd.DataFrame(st.session_state.struct_elements)
        st.dataframe(df[["type", "b", "h", "area"]])
    with col2:
        st.subheader("📑 المذكرة الحسابية")
        st.write(f"تاريخ التصميم: {datetime.date.today()}")
        st.latex(r"A_{min} = 900 \, cm^2")
        if any((df['type']=="Column") & (df['area'] < 900)):
            st.error("🚨 يوجد أعمدة مخالفة للكود!")

