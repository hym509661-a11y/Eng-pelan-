import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# الإعدادات العامة للبرنامج [2026-02-18]
st.set_page_config(page_title="مكتب المهندس بيلان الإنشائي", layout="wide")

# الختم الرسمي الثابت في كامل البرنامج
SEAL = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات 0998449697"

def main():
    # القائمة الجانبية مع الختم
    st.sidebar.title("🏗️ نظام التصميم الإنشائي")
    st.sidebar.markdown(f"---")
    st.sidebar.text(SEAL)
    st.sidebar.markdown(f"---")
    
    menu = [
        "1. المدخلات العامة", 
        "2. البلاطات المصمتة", 
        "3. الجوائز الساقطة", 
        "4. الأعمدة", 
        "5. الهوردي والأعصاب", 
        "6. الجوائز المخفية", 
        "7. الأساسات"
    ]
    choice = st.sidebar.radio("القائمة الرئيسية:", menu)

    # تهيئة الذاكرة المؤقتة (Session State) لربط الصفحات
    if 'fcu' not in st.session_state: st.session_state['fcu'] = 25.0
    if 'fy' not in st.session_state: st.session_state['fy'] = 400.0
    if 'LL' not in st.session_state: st.session_state['LL'] = 2.0
    if 'Cover' not in st.session_state: st.session_state['Cover'] = 1.5

    # توجيه الصفحات
    if choice == "1. المدخلات العامة": show_p1()
    elif choice == "2. البلاطات المصمتة": show_p2()
    elif choice == "3. الجوائز الساقطة": show_p3()
    elif choice == "4. الأعمدة": show_p4()
    elif choice == "5. الهوردي والأعصاب": show_p5()
    elif choice == "6. الجوائز المخفية": show_p6()
    elif choice == "7. الأساسات": show_p7()

# --- الصفحة الأولى: المدخلات العامة ---
def show_p1():
    st.header("📋 الصفحة الأولى: المدخلات العامة")
    st.info(SEAL)
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['fcu'] = st.number_input("إجهاد الخرسانة المميز (fcu) - MPa", value=st.session_state['fcu'])
        st.session_state['fy'] = st.number_input("إجهاد خضوع الحديد (fy) - MPa", value=st.session_state['fy'])
    with col2:
        st.session_state['LL'] = st.number_input("الحمولة الحية (LL) - kN/m²", value=st.session_state['LL'])
        st.session_state['Cover'] = st.number_input("حمولة التغطية (Cover) - kN/m²", value=st.session_state['Cover'])
    st.success("✅ تم حفظ المدخلات بنجاح وسيتم استخدامها في كافة الصفحات.")

# --- الصفحة الثانية: البلاطات المصمتة ---
def show_p2():
    st.header("🏗️ الصفحة الثانية: دراسة البلاطات المصمتة")
    Ly = st.number_input("طول البلاطة Ly (m)", value=5.0)
    Lx = st.number_input("عرض البلاطة Lx (m)", value=4.0)
    phi = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14], index=1)
    
    r = Ly / Lx
    is_one_way = r > 2
    type_txt = "اتجاه واحد (One-Way)" if is_one_way else "اتجاهين (Two-Way)"
    h = np.ceil((Lx * 100) / (30 if is_one_way else 35))
    
    wu = 1.4*(h/100*25 + st.session_state['Cover']) + 1.6*st.session_state['LL']
    mu = (wu * Lx**2 / 8) if is_one_way else ( (r**4/(1+r**4)) * wu * Lx**2 / 8 )
    as_req = (mu * 10**6) / (0.8 * st.session_state['fy'] * (h-2)*10)
    n_bars = max(5, int(np.ceil(as_req / (np.pi*phi**2/4))))

    st.subheader(f"النتيجة: بلاطة {type_txt}")
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.add_patch(patches.Rectangle((0, 0), Lx, Ly, fill=None, lw=2, edgecolor='black'))
    for i in np.linspace(0.2, Lx-0.2, n_bars):
        ax.plot([i, i], [0.1, Ly-0.1], color='red', lw=1, label='T main')
    ax.text(Lx/2, Ly/2, f"{n_bars}Φ{phi}/m'\nh={h}cm", ha='center', fontweight='bold', bbox=dict(facecolor='white', alpha=0.5))
    ax.text(0, -0.4, SEAL, fontsize=8, color='blue')
    plt.axis('off')
    st.pyplot(fig)

# --- الصفحة الثالثة: الجوائز الساقطة ---
def show_p3():
    st.header("📏 الصفحة الثالثة: الجوائز الساقطة")
    bw = st.number_input("عرض الجائز bw (cm)", value=25)
    h = st.number_input("الارتفاع h (cm)", value=60)
    L = st.number_input("المجاز L (m)", value=5.0)
    phi_main = st.selectbox("قطر الحديد الطولي", [14, 16, 18, 20], index=1)
    
    qu = 40.0 # مثال تصعيدي
    mu = (qu * L**2) / 8
    as_req = (mu * 10**6) / (0.8 * st.session_state['fy'] * (h-5)*10)
    n_bars = max(2, int(np.ceil(as_req / (np.pi*phi_main**2/4))))

    fig, ax = plt.subplots(figsize=(4, 6))
    ax.add_patch(patches.Rectangle((0, 0), bw, h, fill=None, lw=3))
    ax.add_patch(patches.Rectangle((2, 2), bw-4, h-4, fill=None, edgecolor='green', lw=1.5)) # كانات
    for i in np.linspace(5, bw-5, n_bars):
        ax.add_patch(plt.Circle((i, 5), 1.5, color='red')) # حديد سفلي
    ax.add_patch(plt.Circle((5, h-5), 1.2, color='red')) # حديد تعليق
    ax.add_patch(plt.Circle((bw-5, h-5), 1.2, color='red'))
    ax.text(bw/2, -8, f"المقطع: {bw}x{h}\nحديد سفلي: {n_bars}Φ{phi_main}\nكانات: Φ8/20cm\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- الصفحة الرابعة: الأعمدة ---
def show_p4():
    st.header("🏢 الصفحة الرابعة: دراسة الأعمدة")
    a = st.number_input("البعد الكبير a (cm)", value=60)
    b = st.number_input("البعد الصغير b (cm)", value=30)
    pu = st.number_input("الحمولة Pu (kN)", value=2000.0)
    
    ag = a * b
    as_min = 0.01 * ag
    n_bars = max(4, int(np.ceil(as_min / (np.pi*16**2/400))))
    if n_bars % 2 != 0: n_bars += 1

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(patches.Rectangle((0, 0), b, a, fill=None, lw=3))
    for i in np.linspace(5, a-5, n_bars//2):
        ax.add_patch(plt.Circle((5, i), 1.5, color='red'))
        ax.add_patch(plt.Circle((b-5, i), 1.5, color='red'))
    ax.text(b/2, -10, f"العمود: {a}x{b}\nالتسليح: {int(n_bars)}Φ16\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- الصفحة الخامسة: الهوردي ---
def show_p5():
    st.header("🧱 الصفحة الخامسة: الهوردي والأعصاب")
    hb = st.selectbox("ارتفاع البلوك", [15, 20, 25], index=1)
    ts = st.number_input("بلاطة التغطية (cm)", value=7)
    L = st.number_input("طول العصب (m)", value=5.0)
    
    st.subheader("رسم مقطع العصب والآجر")
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.add_patch(patches.Rectangle((0, 0), 40, hb, color='gray', alpha=0.3)) # بلوك يسار
    ax.add_patch(patches.Rectangle((52, 0), 40, hb, color='gray', alpha=0.3)) # بلوك يمين
    ax.add_patch(patches.Rectangle((40, 0), 12, hb+ts, fill=None, lw=2)) # عصب
    ax.add_patch(plt.Circle((43, 4), 1.5, color='red'))
    ax.add_patch(plt.Circle((49, 4), 1.5, color='red'))
    ax.text(46, -10, f"عصب هوردي: 2Φ14 سفلي\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- الصفحة السادسة: الجوائز المخفية ---
def show_p6():
    st.header("📏 الصفحة السادسة: الجوائز المخفية")
    bw = st.number_input("عرض الجائز المخفي (cm)", value=100)
    h = st.number_input("الارتفاع (نفس سماكة الهوردي) (cm)", value=27)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.add_patch(patches.Rectangle((0, 0), bw, h, fill=None, lw=3))
    for i in np.linspace(5, bw-5, 10):
        ax.add_patch(plt.Circle((i, 5), 1.5, color='red'))
    ax.text(bw/2, -8, f"جائز مخفي: 10Φ16 سفلي\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- الصفحة السابعة: الأساسات ---
def show_p7():
    st.header("🦶 الصفحة السابعة: الأساسات")
    f_type = st.selectbox("نوع الأساس", ["مفرد عادي", "مشترك", "إجر بطة", "حصيرة"])
    L = st.number_input("طول القاعدة (m)", value=2.2)
    B = st.number_input("عرض القاعدة (m)", value=2.2)
    phi = st.selectbox("قطر حديد الأساس", [14, 16, 18], index=1)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.add_patch(patches.Rectangle((0, 0), B, L, fill=None, lw=3))
    ax.add_patch(patches.Rectangle((B/2-0.2, L/2-0.1), 0.4, 0.2, color='gray')) # عمود
    for i in np.linspace(0.2, B-0.2, 8):
        ax.plot([i, i], [0.1, L-0.1], color='red', lw=1)
    for i in np.linspace(0.2, L-0.2, 8):
        ax.plot([0.1, B-0.1], [i, i], color='red', lw=1)
    ax.text(B/2, -0.3, f"أساس {f_type}: {B}x{L}m\nحديد: 8Φ{phi}/m' بالاتجاهين\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
