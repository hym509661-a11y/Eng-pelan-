import streamlit as st
import ezdxf
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المهندس AI - تحليل المخططات", layout="wide")

# --- محرك تحليل ملف الأوتوكاد ---
def analyze_dxf(file):
    try:
        # قراءة ملف الـ DXF
        doc = ezdxf.read(file)
        msp = doc.modelspace()
        
        lengths = []
        # البحث عن الخطوط في المخطط (بافتراض أنها تمثل البحور أو الجدران)
        for line in msp.query('LINE'):
            start = line.dxf.start
            end = line.dxf.end
            # قانون المسافة بين نقطتين
            dist = math.sqrt((end.x - start.x)**2 + (end.y - start.y)**2)
            lengths.append(dist)
        
        if not lengths:
            return 5.0  # قيمة افتراضية في حال فشل القراءة
        return max(lengths) # إرجاع أطول بحر تم العثور عليه
    except:
        return 5.0

# --- واجهة المستخدم ---
st.title("🏗️ نظام تحليل المخططات المعمارية وتوليد المذكرة")

# --- 1. رفع الملف المعماري ---
st.subheader("📂 خطوة 1: رفع مخطط الأوتوكاد (DXF)")
uploaded_file = st.file_uploader("ارفع ملف المخطط المعماري هنا", type=['dxf'])

L_max = 5.0 # القيمة الافتراضية

if uploaded_file:
    with st.spinner("جاري تحليل المخطط وحساب أطول بحر..."):
        # محاكاة حفظ الملف وفتحه
        with open("temp.dxf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # استخراج أطول بحر من الملف
        L_max = analyze_dxf("temp.dxf")
        st.success(f"✅ تم تحليل المخطط. أطول بحر تم اكتشافه: {L_max:.2f} متر")

# --- 2. إدخال معطيات الطوابق ---
st.divider()
col_inputs, col_results = st.columns([1, 2])

with col_inputs:
    st.header("📋 معطيات المشروع")
    n_floors = st.number_input("عدد الطوابق", 1, 50, 3)
    h_basement = st.number_input("ارتفاع القبو (m)", 3.0, 5.0, 3.5)
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)
    
    st.subheader("🧱 أنواع البلاطات المطلوبة")
    slab_type_repeat = st.selectbox("نوع بلاطة المتكرر", ["هوردي (Ribbed)", "مصمتة (Solid)"])

# --- 3. المذكرة الحسابية الآلية ---
with col_results:
    st.header("📑 المذكرة الحسابية للسماكات")
    
    # حساب سماكة القبو (دائماً مصمتة للأحمال العالية)
    t_basement = math.ceil((L_max * 100) / 30)
    t_basement = max(t_basement, 15)
    
    # حساب سماكة المتكرر
    if slab_type_repeat == "هوردي (Ribbed)":
        t_repeat = math.ceil((L_max * 100) / 21)
        t_repeat = max(t_repeat, 25)
        eq_repeat = r"t = \frac{L_{max}}{21}"
    else:
        t_repeat = math.ceil((L_max * 100) / 32)
        t_repeat = max(t_repeat, 12)
        eq_repeat = r"t = \frac{L_{max}}{32}"

    # عرض المذكرة باستخدام LaTeX
    st.write("### أولاً: بلاطة القبو (Solid Slab)")
    st.latex(r"t = \frac{L_{max}}{30} = \frac{" + f"{L_max:.2f}" + r" \times 100}{30} = " + f"{t_basement}" + r" \text{ cm}")
    
    st.write(f"### ثانياً: بلاطة الطوابق المتكررة ({slab_type_repeat})")
    st.latex(eq_repeat + r" = \frac{" + f"{L_max:.2f}" + r" \times 100}{" + ("21" if "Ribbed" in slab_type_repeat else "32") + r"} = " + f"{t_repeat}" + r" \text{ cm}")

    

# --- 4. جداول التسليح النهائية ---
st.divider()
st.header("📋 جداول التسليح التفصيلية بناءً على التحليل")

tab1, tab2 = st.tabs(["جداول العناصر", "الرسومات الإنشائية"])

with tab1:
    st.table({
        "الطابق": ["القبو", "الأرضي", "المتكرر"],
        "نوع البلاطة": ["مصمتة (Solid)", slab_type_repeat, slab_type_repeat],
        "السماكة (cm)": [t_basement, t_repeat+2, t_repeat],
        "التسليح المقترح": ["T12 @ 15cm", "2 T14 / Rib", "2 T12 / Rib"]
    })

with tab2:
    st.write("### تفصيل مقطع العمود (لأكبر حمل تراكمي)")
    # حساب حمل تقريبي للأعمدة
    area_tribute = (L_max * L_max) / 2
    p_total = area_tribute * 1.2 * n_floors # طن تقريبي
    
    c_dim = math.ceil(p_total / 10) * 10 # عرض العمود التقريبي
    st.write(f"العمود المقترح للقبو: 30x{max(c_dim, 50)} cm")
    

if st.button("🚀 تصدير المذكرة والمخططات"):
    st.download_button("تحميل المذكرة الحسابية PDF", "محتوى المذكرة...", file_name="Structural_Report.pdf")
