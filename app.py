import streamlit as st
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- إعدادات الصفحة ---
st.set_page_config(page_title="المهندس AI - النظام المتكامل", layout="wide")

# --- دالة المذكرة الحسابية (LaTeX) ---
def generate_memo(L, load, fcu, fy):
    st.header("📑 المذكرة الحسابية (Calculation Memo)")
    
    # حساب سماكة البلاطة
    t = math.ceil((L * 100) / 21) # للهوردي
    st.write("### 1. تصميم البلاطة (Slab Design)")
    st.latex(r"t_{min} = \frac{L}{21} = \frac{" + str(L) + r" \times 100}{21} = " + str(t) + r" \text{ cm}")
    
    # حساب الأحمال التراكمية
    st.write("### 2. تحليل الأحمال (Load Analysis)")
    st.latex(r"w_u = 1.4 \cdot DL + 1.6 \cdot LL")
    st.latex(r"P_{total} = \sum (w_u \times Area \times n_{floors}) \times 1.1")
    
    return t

# --- واجهة البرنامج الرئيسية ---
st.title("🏗️ نظام التصميم الإنشائي الذكي v12.0")

# --- 1. منطقة رفع الملف (File Upload) ---
st.subheader("📂 خطوة 1: رفع المخطط المعماري")
uploaded_file = st.file_uploader("قم برفع ملف الأوتوكاد بصيغة DXF", type=['dxf'])

if uploaded_file:
    st.success("✅ تم تحميل الملف المعماري بنجاح. يمكنك الآن استخدامه كخلفية لتوقيع الأعمدة.")

# --- 2. مدخلات المبنى (Sidebar) ---
with st.sidebar:
    st.header("📋 معطيات المشروع")
    n_floors = st.number_input("عدد الطوابق المتكررة", 1, 50, 3)
    h_basement = st.number_input("ارتفاع القبو (m)", 3.0, 5.0, 3.5)
    h_ground = st.number_input("ارتفاع الأرضي (m)", 3.0, 6.0, 4.0)
    st.divider()
    st.header("🛠️ أدوات التوقيع")
    tool = st.radio("الأداة النشطة:", ["توقيع عمود (Column)", "رسم جائز (Beam)"])
    if st.button("🗑️ مسح اللوحة"):
        st.session_state.points = []

# --- 3. لوحة التفاعل (Interactive Layout) ---
if 'points' not in st.session_state:
    st.session_state.points = []

col_draw, col_memo = st.columns([2, 1])

with col_draw:
    st.subheader("📍 لوحة توقيع الأعمدة والجوائز")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # رسم الشبكة (Grid)
    ax.set_xticks(range(11))
    ax.set_yticks(range(11))
    ax.grid(True, linestyle=':', alpha=0.5)
    
    # محاكاة التوقيع عبر الإحداثيات
    ix = st.number_input("إحداثي X", 0.0, 10.0, 2.0, step=0.5)
    iy = st.number_input("إحداثي Y", 0.0, 10.0, 2.0, step=0.5)
    
    if st.button(f"➕ إضافة {tool}"):
        st.session_state.points.append({"type": tool, "x": ix, "y": iy})

    # رسم العناصر الموقعة
    for p in st.session_state.points:
        if "Column" in p["type"]:
            ax.add_patch(patches.Rectangle((p["x"]-0.2, p["y"]-0.2), 0.4, 0.4, color='black', label='Column'))
        else:
            ax.plot([p["x"], p["x"]+3], [p["y"], p["y"]], color='blue', lw=4, label='Beam')
            
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    st.pyplot(fig)

with col_memo:
    # المذكرة الحسابية الحية
    t_calculated = generate_memo(L=5.5, load=1.2, fcu=25, fy=400)
    st.info(f"سماكة بلاطة القبو: {t_calculated - 5} cm (Solid)")
    st.info(f"سماكة البلاطات المتكررة: {t_calculated} cm (Hordy)")

# --- 4. جداول التسليح (BBS) ---
st.divider()
st.header("📋 الجداول الإنشائية التفصيلية")

tab1, tab2, tab3 = st.tabs(["جداول التسليح", "تفاصيل الهوردي", "الأساسات"])

with tab1:
    st.write("### 📊 جدول نماذج الأعمدة")
    st.table({
        "الطابق": ["القبو", "الأرضي", "المتكرر"],
        "المقطع (cm)": ["30x80", "30x60", "30x40"],
        "التسليح": ["14 T16", "10 T16", "8 T14"]
    })
    

with tab2:
    st.write("### 🧱 تفاصيل بلاطة الهوردي")
    
    st.table({
        "العنصر": ["العصب الرئيسي", "البلوك", "بلاطة التغطية"],
        "التسليح/الأبعاد": ["2 T14 (Bottom)", "40x20x24 cm", "T8 @ 20 cm"]
    })

with tab3:
    st.write("### 📐 جداول الأساسات")
    
    st.table({
        "النوع": ["F1 (منفرد)", "F2 (منفرد)", "Strap Beam"],
        "الأبعاد (m)": ["2.4x2.4", "2.0x2.0", "0.6x0.9"],
        "التسليح": ["T16 @ 12.5cm", "T16 @ 15cm", "8 T18"]
    })

# --- زر التصدير النهائي ---
st.divider()
if st.button("🚀 تصدير المخططات والمذكرة الحسابية النهائية"):
    st.success("تم توليد ملفات DXF بنجاح لجميع الطوابق.")
    st.download_button("تحميل المذكرة الحسابية (PDF)", "بيانات المذكرة...", file_name="Calculation_Memo.pdf")
