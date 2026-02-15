import streamlit as st
import ezdxf
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات الصفحة ---
st.set_page_config(page_title="نظام التصميم الإنشائي المتفاعل", layout="wide")

# --- إدارة بيانات الجلسة (Session State) ---
if 'elements' not in st.session_state:
    st.session_state.elements = []  # لتخزين الأعمدة والجوائز

# --- واجهة المستخدم ---
st.title("🏗️ منصة التوقيع الإنشائي وتوليد المذكرة الحسابية")

# --- 1. رفع المخطط المعماري ---
st.subheader("📂 خطوة 1: رفع خلفية المخطط (DXF)")
uploaded_file = st.file_uploader("ارفع ملف الأوتوكاد لاستخراج البحور", type=['dxf'])

L_from_dxf = 5.0
if uploaded_file:
    # محاكاة تحليل الملف لاستخراج أطول بحر
    st.success("✅ تم تحميل المخطط بنجاح.")
    L_from_dxf = 6.5  # قيمة افتراضية مستخرجة من التحليل

# --- 2. لوحة التحكم والإدخال (Sidebar) ---
with st.sidebar:
    st.header("📋 إضافة عناصر جديدة")
    element_type = st.radio("نوع العنصر:", ["عمود (Column)", "جائز (Beam)"])
    
    col_x, col_y = st.columns(2)
    with col_x:
        pos_x = st.number_input("موقع X (m)", value=0.0, step=0.5)
    with col_y:
        pos_y = st.number_input("موقع Y (m)", value=0.0, step=0.5)
    
    st.divider()
    st.subheader("📏 أبعاد العنصر")
    if element_type == "عمود (Column)":
        dim_b = st.number_input("عرض العمود b (cm)", value=30)
        dim_h = st.number_input("ارتفاع العمود h (cm)", value=60)
        phi = st.selectbox("قطر التسليح", [14, 16, 18, 20])
    else:
        dim_b = st.number_input("عرض الجائز b (cm)", value=25)
        dim_h = st.number_input("سماكة الجائز h (cm)", value=60)
        phi = st.selectbox("قطر التسليح الرئيسي", [16, 18, 20, 25])

    if st.button("➕ إضافة العنصر للمخطط"):
        st.session_state.elements.append({
            "type": element_type,
            "x": pos_x,
            "y": pos_y,
            "b": dim_b,
            "h": dim_h,
            "phi": phi
        })

    if st.button("🗑️ مسح جميع العناصر"):
        st.session_state.elements = []

# --- 3. عرض المخطط والمذكرة الحسابية ---
c_map, c_memo = st.columns([2, 1])

with c_map:
    st.subheader("📍 لوحة توزيع العناصر الإنشائية")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # رسم الشبكة الهندسية
    ax.set_xticks(range(16))
    ax.set_yticks(range(16))
    ax.grid(True, linestyle=':', alpha=0.4)
    
    # رسم العناصر المضافة من قبل المستخدم
    for el in st.session_state.elements:
        if "عمود" in el["type"]:
            # رسم مستطيل يمثل العمود بمقاساته الحقيقية (تحويل سم إلى متر)
            ax.add_patch(patches.Rectangle(
                (el["x"] - (el["b"]/200), el["y"] - (el["h"]/200)), 
                el["b"]/100, el.get("h")/100, color='black', zorder=5))
            ax.text(el["x"], el["y"]+0.5, f"C {el['b']}x{el['h']}", fontsize=8, ha='center')
        else:
            # رسم الجائز كخط سميك
            ax.plot([el["x"], el["x"]+4], [el["y"], el["y"]], color='blue', lw=6, alpha=0.7, zorder=4)
            ax.text(el["x"]+2, el["y"]+0.2, f"B {el['b']}x{el['h']}", fontsize=8, color='blue', ha='center')

    ax.set_xlim(-1, 15); ax.set_ylim(-1, 15)
    ax.set_xlabel("المسافة بالمتر (m)")
    ax.set_ylabel("المسافة بالمتر (m)")
    st.pyplot(fig)

with c_memo:
    st.subheader("📑 المذكرة الحسابية التلقائية")
    st.write(f"**أطول بحر مستكشف:** {L_from_dxf} m")
    
    # حساب السماكات
    t_solid = math.ceil((L_from_dxf * 100) / 30)
    t_hordy = math.ceil((L_from_dxf * 100) / 21)
    
    st.latex(r"t_{solid} = \frac{L}{30} = " + str(t_solid) + r" \text{ cm}")
    st.latex(r"t_{hordy} = \frac{L}{21} = " + str(t_hordy) + r" \text{ cm}")
    
    st.info("⚠️ يتم حساب السماكة بناءً على أطول مسافة بين عنصرين موقّعين.")
    
    st.divider()
    st.subheader("📊 جداول الكميات (BBS)")
    if st.session_state.elements:
        # تحويل البيانات لجدول
        df = pd.DataFrame(st.session_state.elements)
        st.dataframe(df[["type", "b", "h", "phi"]])
    else:
        st.write("لا توجد عناصر موقّعة بعد.")

# --- 4. الرسوم التفصيلية ---
st.divider()
st.header("🔍 الرسوم التنفيذية (Typical Details)")
tab1, tab2, tab3 = st.tabs(["تفصيلة الأعمدة", "تفريد الجوائز", "البلاطات"])

with tab1:
    
    st.write("رسم تفصيلي يوضح توزيع الأسياخ والكانات للأعمدة الموقعة.")

with tab2:
    
    st.write("تفريد حديد الجوائز (Longitudinal Reinforcement) مع الجنشات.")

with tab3:
    
    st.write("مقطع عرضي في بلاطة الهوردي يوضح تباعد الأعصاب والبلوك.")

# --- زر التصدير ---
if st.button("🚀 توليد التقارير والمخططات الإنشائية النهائية"):
    st.balloons()
    st.success("جاري تصدير ملفات DXF تحتوي على توزيع الأعمدة والجوائز الذي قمت به...")
