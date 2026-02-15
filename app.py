import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات واجهة البرنامج
st.set_page_config(page_title="المصمم الإنشائي الذكي", layout="wide")

st.title("🏗️ منصة التوقيع الإنشائي وتحديد مساحات البلاطات")

# --- القائمة الجانبية (الأدوات) ---
with st.sidebar:
    st.header("📋 معطيات المشروع")
    eng_name = st.text_input("اسم المهندس المصمم", "المهندس/ .................")
    
    st.divider()
    st.header("🖼️ المخطط المعماري")
    # زر إضافة المخطط كخلفية
    bg_image = st.file_uploader("ارفع صورة المخطط المعماري (JPG/PNG)", type=['png', 'jpg', 'jpeg'])
    
    st.divider()
    st.header("🛠️ أدوات الرسم")
    tool = st.radio("العنصر الحالي:", ["عمود (Column)", "جائز (Beam)", "بلاطة هوردي", "بلاطة مصمتة"])
    b_cm = st.number_input("العرض b (cm)", 30)
    h_cm = st.number_input("الارتفاع/السمك h (cm)", 60)

# --- إدارة البيانات (تخزين النقاط) ---
if 'drawing_elements' not in st.session_state:
    st.session_state.drawing_elements = []

# --- لوحة الرسم التفاعلية ---
col_map, col_memo = st.columns([2, 1])

with col_map:
    st.subheader("📍 لوحة التوقيع (انقر لتحديد الإحداثيات)")
    
    # محاكاة إحداثيات النقرة بالماوس
    c1, c2 = st.columns(2)
    with c1: x_click = st.number_input("موقع X (m)", 0.0, 50.0, step=0.1)
    with c2: y_click = st.number_input("موقع Y (m)", 0.0, 50.0, step=0.1)

    if st.button("✅ تثبيت العنصر في هذا المكان"):
        # التدقيق الإنشائي (إنذار الـ 900 سم2)
        area = b_cm * h_cm
        status = "آمن"
        if "عمود" in tool and area < 900:
            st.error(f"🚨 إنذار: المقطع {area}cm² أصغر من الحد الأدنى 900cm²!")
            status = "🚨 مخالف"
        
        st.session_state.drawing_elements.append({
            "نوع": tool, "x": x_click, "y": y_click, "b": b_cm, "h": h_cm, "الحالة": status
        })

    # إنشاء المخطط
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # وضع الخلفية المعمارية إذا تم رفعها
    if bg_image:
        import matplotlib.image as mpimg
        img = mpimg.imread(bg_image)
        ax.imshow(img, extent=[0, 20, 0, 20], alpha=0.5)
    else:
        ax.set_facecolor('#2b2b2b') # خلفية سوداء (أوتوكاد)

    # رسم العناصر الموقعة
    for el in st.session_state.drawing_elements:
        if "عمود" in el["نوع"]:
            color = 'red' if "مخالف" in el["الحالة"] else 'white'
            ax.add_patch(patches.Rectangle((el["x"]-0.2, el["y"]-0.2), 0.4, 0.4, color=color))
        elif "جائز" in el["نوع"]:
            ax.plot([el["x"], el["x"]+3], [el["y"], el["y"]], color='cyan', lw=3)
        elif "هوردي" in el["نوع"]:
            ax.add_patch(patches.Rectangle((el["x"], el["y"]), 4, 3, hatch='///', edgecolor='yellow', fill=False))
        elif "مصمتة" in el["نوع"]:
            ax.add_patch(patches.Rectangle((el["x"], el["y"]), 4, 3, facecolor='blue', alpha=0.2))

    ax.set_xlim(0, 20); ax.set_ylim(0, 20)
    st.pyplot(fig)

with col_memo:
    st.subheader("📑 المذكرة وجدول الكميات")
    st.write(f"**المصمم:** {eng_name}")
    if st.session_state.drawing_elements:
        df = pd.DataFrame(st.session_state.drawing_elements)
        st.table(df[["نوع", "b", "h", "الحالة"]])
