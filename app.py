import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# بيانات الختم
STAMP_TEXT = "الالمهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات | 0998449697"

def calculate_as(M_un, d, b, fcu, fy):
    """حساب مساحة التسليح المطلوبة وفق الكود (Simplified Method)"""
    if M_un <= 0: return 0
    # حساب قيمة Rn (k في بعض المراجع)
    Rn = (M_un * 10**6) / (b * 10 * (d * 10)**2)
    # حساب نسبة التسليح rho تقريبياً
    m = fy / (0.85 * fcu)
    rho = (1/m) * (1 - np.sqrt(1 - (2 * m * Rn) / fy))
    as_req = rho * b * 10 * d * 10 / 100 # cm2
    return max(as_req, 0.0015 * b * d) # الحد الأدنى للكود

def get_bars_count(as_required, phi):
    """تحويل المساحة المطلوبة إلى عدد أسياخ حقيقي"""
    if as_required <= 0: return 2
    as_single_bar = (np.pi * phi**2) / 400 # مساحة السيخ الواحد بـ cm2
    count = np.ceil(as_required / as_single_bar)
    return int(max(count, 2)) # لا يقل عن سيخين

# إعدادات الواجهة
st.set_page_config(page_title="برنامج الجواد - نسخة المهندس بيلان", layout="wide")
st.title("🏗️ المصمم الإنشائي الآلي (حساب التفريد)")

with st.sidebar:
    st.header("⚙️ معطيات الكود")
    fcu = st.number_input("إجهاد البيتون fcu (MPa)", value=25)
    fy = st.number_input("إجهاد الفولاذ fy (MPa)", value=400)
    phi = st.selectbox("قطر السيخ المستخدم (mm)", [12, 14, 16, 18, 20, 25])
    st.markdown("---")
    st.header("📏 أبعاد المقطع (cm)")
    b = st.number_input("العرض b", value=30)
    h = st.number_input("الارتفاع h", value=60)
    d = h - 5 # العمق الفعال

st.subheader("📊 حسابات الجوائز (العزوم والقص)")
col1, col2 = st.columns([1, 2])

with col1:
    L = st.number_input("طول المجاز (m)", value=5.0)
    w = st.number_input("الحمولة التصميمية الموزعة (kN/m)", value=40.0)
    
    # حساب العزوم (حسابي آلي)
    M_max = (w * L**2) / 8 # عزم موجب (سفلي)
    M_top = M_max * 0.15   # عزم تعليق علوي (افتراضي لربط الأساور)
    
    # حساب مساحة الحديد المطلوبة (حسابي)
    as_bot_req = calculate_as(M_max, d, b, fcu, fy)
    as_top_req = as_bot_req * 0.2 # حديد التعليق 20% من الرئيسي أو حسب الكود
    
    # تحويل المساحة إلى عدد أسياخ (آلي)
    n_bot = get_bars_count(as_bot_req, phi)
    n_top = get_bars_count(as_top_req, phi)
    
    st.write(f"**العزم المحسوب:** {M_max:.2f} kN.m")
    st.write(f"**مساحة الحديد السفلي:** {as_bot_req:.2f} cm²")
    st.success(f"**النتيجة:** استخدم {n_bot} T {phi} (سفلي)")
    st.info(f"**التعليق:** استخدم {n_top} T {phi} (علوي)")

with col2:
    # رسم المقطع آلياً بناءً على الحسابات
    from matplotlib.patches import Rectangle, Circle
    fig, ax = plt.subplots(figsize=(4, 5))
    ax.add_patch(Rectangle((0, 0), b, h, color='#f0f0f0')) # الخرسانة
    cover = 3.5
    
    # رسم الحديد السفلي المحسوب
    x_bot = np.linspace(cover, b-cover, n_bot)
    for x in x_bot:
        ax.add_patch(Circle((x, cover), 0.8, color='red'))
        
    # رسم الحديد العلوي المحسوب
    x_top = np.linspace(cover, b-cover, n_top)
    for x in x_top:
        ax.add_patch(Circle((x, h-cover), 0.8, color='blue'))
        
    ax.set_xlim(-5, b+5); ax.set_ylim(-5, h+5); ax.set_aspect('equal')
    plt.title("تفريد الحديد المحسوب آلياً")
    st.pyplot(fig)

# الختم
st.markdown("---")
st.text(STAMP_TEXT)
