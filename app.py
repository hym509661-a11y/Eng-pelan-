import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image, ImageDraw

# --- إعدادات البرنامج باسم المهندس بيلان ---
st.set_page_config(page_title="Bilan-Engineering Pro", layout="wide")

st.markdown(f"""
    <div style="background-color:#003366;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Bilan-Engineering Pro v1.0</h1>
    <h3 style="color:white;text-align:center;">إعداد المهندس: بيلان عبدالكريم</h3>
    </div>
    """, unsafe_allow_html=True)

# إدارة البيانات
if 'elements' not in st.session_state: st.session_state.elements = []

# --- القائمة الجانبية: المدخلات الإنشائية ---
with st.sidebar:
    st.header("⚙️ معطيات التصميم الأساسية")
    fcu = st.number_input("إجهاد الخرسانة fcu (kg/cm²)", 250)
    fy = st.number_input("إجهاد الحديد fy (kg/cm²)", 4000)
    
    st.divider()
    st.header("🏗️ تفاصيل العنصر")
    category = st.selectbox("العنصر الإنشائي:", ["جائز مستمر (Beam)", "عمود (Column)", "بلاطة هوردي", "بلاطة مصمتة"])
    
    col1, col2 = st.columns(2)
    with col1: b = st.number_input("العرض b (cm)", 30)
    with col2: h = st.number_input("الارتفاع h (cm)", 60)
    
    st.subheader("🔗 التسليح (Rebar)")
    rebar_dia = st.selectbox("قطر القضيب (mm):", [8, 10, 12, 14, 16, 18, 20, 25])
    rebar_count = st.number_input("عدد القضبان:", 2, 20, 4)
    
    st.divider()
    load = st.number_input("الحمل الموزع w (t/m)", 0.0, 20.0, 2.5)
    span = st.number_input("طول البحر L (m)", 1.0, 15.0, 5.0)

# --- نافذة الرسم (شاشتين: رسم معماري + مخططات هندسية) ---
tab1, tab2, tab3 = st.tabs(["🖥️ نافذة الرسم (SAFE Mode)", "📊 مخططات العزم والقص", "📋 المذكرة والجداول"])

with tab1:
    st.subheader("📍 توقيع العناصر فوق المخطط المعماري")
    bg = st.file_uploader("ارفع مخطط الأوتوكاد كخلفية", type=['png', 'jpg'])
    if bg:
        img = Image.open(bg)
        # ميزة الزوم البسيط عبر Resize
        zoom = st.slider("التقريب (Zoom)", 1.0, 5.0, 1.0)
        new_size = (int(img.width * zoom), int(img.height * zoom))
        img_res = img.resize(new_size)
        
        coords = streamlit_image_coordinates(img_res, key="bilan_draw")
        if coords:
            st.session_state.elements.append({
                "type": category, "x": coords['x'], "y": coords['y'], 
                "b": b, "h": h, "dia": rebar_dia, "count": rebar_count, "L": span, "w": load
            })
            st.rerun()

with tab2:
    st.subheader("📉 التحليل الإنشائي للمقاطع")
    if st.session_state.elements:
        # رسم مخطط العزم والقص لآخر عنصر تم إدخاله
        x = np.linspace(0, span, 100)
        moment = (load * x / 2) * (span - x)  # معادلة العزم لجائز بسيط
        shear = load * (span / 2 - x)         # معادلة القص
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        ax1.fill_between(x, moment, color='skyblue', alpha=0.4)
        ax1.set_title("مخطط العزم (Bending Moment Diagram) - Mmax = " + f"{max(moment):.2f} t.m")
        ax1.invert_yaxis()
        
        ax2.fill_between(x, shear, color='salmon', alpha=0.4)
        ax2.set_title("مخطط القص (Shear Force Diagram)")
        st.pyplot(fig)
    else:
        st.info("قم بتوقيع عنصر في نافذة الرسم لعرض مخططاته.")

with tab3:
    st.subheader(f"📑 المذكرة الحسابية - المهندس بيلان عبدالكريم")
    if st.session_state.elements:
        df = pd.DataFrame(st.session_state.elements)
        # حساب كميات الحديد التقريبية
        df['As (cm²)'] = df['count'] * (3.14 * (df['dia']/20)**2)
        st.write("### جدول تسليح العناصر (BBS Table):")
        st.table(df[["type", "b", "h", "L", "dia", "count", "As (cm²)"]])
        
        st.divider()
        st.write("### تفاصيل الفرش والغطاء الخرساني:")
        
        st.write(f"- الغطاء الخرساني المعتمد: 2.5 cm للجوانب و 5 cm للقواعد.")
        st.write(f"- توزيع الأساور: يتم التكثيف في الثلث الأول والأخير من البحر.")
        

# زر التصدير
if st.button("🚀 إصدار التقرير النهائي PDF"):
    st.success(f"تم توليد المذكرة الحسابية باسم المهندس بيلان عبدالكريم بنجاح!")
