import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- الترويسة الهندسية ---
st.set_page_config(page_title="Bilan-Engineering Pro", layout="wide")
st.markdown(f"<h1 style='text-align: center; color: #1E3A8A;'>Bilan Integrated Design Suite</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center;'>المهندس المصمم: بيلان عبدالكريم</h3>", unsafe_allow_html=True)
st.divider()

# --- مدخلات النظام ---
with st.sidebar:
    st.header("📂 اختيار العنصر الإنشائي")
    element_type = st.selectbox("نوع العنصر", 
        ["بلاطة مصمتة (Solid Slab)", "بلاطة هوردي (Ribbed Slab)", "أساس منفرد (Isolated Footing)", "أساس مشترك (Combined Footing)", "جائز (Beam)", "عمود (Column)"])
    
    st.divider()
    st.header("📐 الأبعاد والأحمال")
    L_span = st.number_input("طول البحر L (m)", value=5.0)
    B_width = st.number_input("العرض B (m)", value=4.0)
    thickness = st.number_input("السماكة t (cm)", value=15 if "Solid" in element_type else 25)
    
    q_all = st.number_input("تحمل التربة (kg/cm²)", value=2.0) if "Footing" in element_type else 0.0
    load_u = st.number_input("الحمل التصميمي (t/m² أو t)", value=1.2 if "Slab" in element_type else 100.0)

# --- المحرك الحسابي الذكي ---
def calculate_design(element, L, B, t, load):
    results = {}
    fy = 4000
    
    if "Solid" in element:
        # تصميم بلاطة مصمتة
        M_u = (load * L**2) / 8
        As = (M_u * 10**5) / (0.87 * fy * (t-3))
        results = {"العزم (t.m)": round(M_u, 2), "التسليح المطلوب As (cm²/m)": round(As, 2), "الفرش": f"T12@{200/As*1.13:.0f}mm"}
        
    elif "Ribbed" in element:
        # تصميم بلاطة هوردي
        M_rib = (load * 0.52 * L**2) / 8 # عرض العصب 52 سم
        As_rib = (M_rib * 10**5) / (0.87 * fy * (t-5))
        results = {"عزم العصب (t.m)": round(M_rib, 2), "تسليح العصب": f"{int(np.ceil(As_rib/1.13))} T12"}
        
    elif "Isolated" in element:
        # تصميم أساس منفرد
        Area_req = (load / (q_all * 10)) * 1.1 # زيادة 10% للوزن الذاتي
        side = np.sqrt(Area_req)
        results = {"مساحة القاعدة (m²)": round(Area_req, 2), "الأبعاد": f"{side:.2f} x {side:.2f} m"}
        
    return results

res = calculate_design(element_type, L_span, B_width, thickness, load_u)

# --- العرض المرئي والمذكرة ---
col_res, col_img = st.columns([1, 1])

with col_res:
    st.subheader("📊 النتائج الحسابية")
    for key, value in res.items():
        st.metric(label=key, value=value)
    
    st.divider()
    st.subheader("📝 المذكرة الحسابية - بيلان عبدالكريم")
    st.write(f"بناءً على الكود السوري، تم تصميم **{element_type}** بالأبعاد المعطاة.")
    if "Slab" in element_type:
        st.write("- يتم توزيـع حديد الفرش في الاتجاه القصير.")
        st.write("- يتم وضع كراسي لضمان ثبات الغطاء الخرساني.")
    elif "Footing" in element_type:
        st.write("- يتم صب طبقة نظافة بسماكة 10 سم قبل البدء بالتسليح.")

with col_img:
    st.subheader("🎨 مخططات الفرش والتسليح")
    if "Solid" in element_type:
        
    elif "Ribbed" in element_type:
        
    elif "Footing" in element_type:
        
    elif "Column" in element_type:
        

# --- رسم توضيحي للمقطع ---
fig, ax = plt.subplots(figsize=(6, 4))
if "Footing" in element_type:
    ax.add_patch(patches.Rectangle((0.5, 0.5), 2, 0.5, facecolor='gray', edgecolor='black'))
    ax.add_patch(patches.Rectangle((1.25, 1.0), 0.5, 1.5, facecolor='darkgray', edgecolor='black'))
    ax.set_title("مقطع جانبي في الأساس والرقبة")
else:
    ax.add_patch(patches.Rectangle((0.1, 0.1), 0.8, 0.2, facecolor='lightgrey', edgecolor='black'))
    ax.set_title(f"مقطع عرضي في {element_type}")
ax.axis('off')
st.pyplot(fig)
