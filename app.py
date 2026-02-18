import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# بيانات الختم المحفوظة
STAMP_TEXT = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات | 0998449697"

def draw_detailed_section(b, h, bot_bars, top_bars, add_bars):
    fig, ax = plt.subplots(figsize=(5, 6))
    # رسم بيتون الجائز
    rect = plt.Rectangle((0, 0), b, h, color='#E0E0E0', label='Concrete')
    ax.add_patch(rect)
    
    cover = 3.0
    # رسم الأساور (Stirrups)
    stirrup = plt.Rectangle((cover/2, cover/2), b-cover, h-cover, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(stirrup)

    # دالة لرسم الأسياخ
    def plot_bars(count, y_pos, color, label):
        if count > 0:
            x_space = np.linspace(cover + 1, b - cover - 1, count)
            for x in x_space:
                circle = plt.Circle((x, y_pos), 0.8, color=color)
                ax.add_patch(circle)

    # 1. الحديد السفلي (الرئيسي) - باللون الأحمر
    plot_bars(bot_bars, cover + 1, 'red', 'سفلي')
    
    # 2. الحديد العلوي (التعليق) - باللون الأزرق
    plot_bars(top_bars, h - cover - 1, 'blue', 'تعليق')
    
    # 3. الحديد الإضافي (إن وجد) - باللون الأخضر
    if add_bars > 0:
        plot_bars(add_bars, cover + 3.5, 'green', 'إضافي')

    ax.set_xlim(-5, b + 5)
    ax.set_ylim(-5, h + 5)
    ax.set_aspect('equal')
    plt.title(f"تفصيل تسليح المقطع ({b}x{h})")
    return fig

st.set_page_config(page_title="برنامج المهندس بيلان - التفريد الدقيق")
st.title("🏗️ نظام تفريد الحديد الاحترافي")

with st.sidebar:
    st.header("بيانات المقطع")
    b = st.number_input("عرض الجائز (cm)", value=30)
    h = st.number_input("ارتفاع الجائز (cm)", value=60)
    st.markdown("---")
    st.header("حسابات التسليح")
    fcu = st.number_input("fcu (MPa)", value=25)
    fy = st.number_input("fy (MPa)", value=400)

col1, col2 = st.columns(2)

with col1:
    st.subheader("إدخال عدد الأسياخ")
    n_bot = st.number_input("عدد الأسياخ السفلية (الرئيسية)", min_value=2, value=4)
    n_top = st.number_input("عدد أسياخ التعليق (علوية)", min_value=2, value=2)
    n_add = st.number_input("عدد الأسياخ الإضافية", min_value=0, value=0)
    phi = st.selectbox("قطر السيخ المستخدم (mm)", [12, 14, 16, 18, 20, 25])

with col2:
    st.subheader("الرسم الهندسي")
    fig = draw_detailed_section(b, h, n_bot, n_top, n_add)
    st.pyplot(fig)

# منطقة النتائج الفنية
as_total = (n_bot + n_add) * (np.pi * (phi/10)**2 / 4)
st.success(f"مساحة التسليح المحققة: {as_total:.2f} cm²")

# طباعة الختم في نهاية كل صفحة
st.markdown("---")
st.text_area("الختم الرسمي للمشروع", STAMP_TEXT, height=70)

if st.button("توليد تقرير PDF للطباعة"):
    st.info("جاري تجهيز التقرير بختم المهندس بيلان...")
