import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# الختم الرسمي [2026-02-18]
SEAL = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات 0998449697"

def main():
    st.sidebar.title("🏢 نظام التصميم المتكامل")
    st.sidebar.info(SEAL)
    
    pages = [
        "1. المدخلات العامة", "2. البلاطات المصمتة", "3. الجوائز الساقطة",
        "4. الأعمدة", "5. الهوردي والأعصاب", "6. الجوائز المخفية", "7. الأساسات"
    ]
    choice = st.sidebar.radio("انتقل إلى الدراسة:", pages)

    # تهيئة المتغيرات في حالة عدم وجودها
    if 'fcu' not in st.session_state: st.session_state['fcu'] = 25.0
    if 'fy' not in st.session_state: st.session_state['fy'] = 400.0

    if choice == "1. المدخلات العامة":
        show_p1()
    elif choice == "2. البلاطات المصمتة":
        show_p2()
    elif choice == "3. الجوائز الساقطة":
        show_p3()
    elif choice == "4. الأعمدة":
        show_p4()
    elif choice == "5. الهوردي والأعصاب":
        show_p5()
    elif choice == "6. الجوائز المخفية":
        show_p6()
    elif choice == "7. الأساسات":
        show_p7()

# --- 1. الصفحة الأولى: المدخلات العامة ---
def show_p1():
    st.header("📋 المدخلات العامة للمشروع")
    st.markdown(f"**إشراف: {SEAL}**")
    col1, col2 = st.columns(2)
    with col1:
        st.session_state['fcu'] = st.number_input("إجهاد الخرسانة (fcu) - MPa", value=25.0)
        st.session_state['fy'] = st.number_input("إجهاد خضوع الحديد (fy) - MPa", value=400.0)
    with col2:
        st.session_state['LL'] = st.number_input("الحمولة الحية (LL) - kN/m²", value=2.0)
        st.session_state['Cover'] = st.number_input("حمولة التغطية (Cover) - kN/m²", value=1.5)
    st.success("تم تثبيت البيانات العامة للمشروع.")

# --- 2. الصفحة الثانية: البلاطات المصمتة ---
def show_p2():
    st.header("🏗️ دراسة البلاطات المصمتة")
    col1, col2 = st.columns(2)
    with col1:
        Ly = st.number_input("طول الفتحة Ly (m)", value=5.0)
        Lx = st.number_input("عرض الفتحة Lx (m)", value=4.0)
    with col2:
        phi = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14], index=1)
        h = st.number_input("سماكة البلاطة المنفذة (cm)", value=15)

    r = Ly / Lx
    is_one_way = r > 2
    slab_type = "اتجاه واحد" if is_one_way else "اتجاهين"
    
    # الحسابات
    wu = 1.4*(h/100*25 + st.session_state['Cover']) + 1.6*st.session_state['LL']
    mu = (wu * Lx**2 / 8) if is_one_way else ( (r**4/(1+r**4)) * wu * Lx**2 / 8 )
    as_req = (mu * 10**6) / (0.8 * st.session_state['fy'] * (h-2)*10)
    n_bars = max(5, int(np.ceil(as_req / (np.pi*phi**2/4))))

    # الرسم
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.add_patch(patches.Rectangle((0, 0), Lx, Ly, fill=None, lw=2))
    # رسم الأسياخ
    for i in np.linspace(0.2, Lx-0.2, n_bars):
        ax.plot([i, i], [0.1, Ly-0.1], color='red', lw=1)
    ax.text(Lx/2, Ly/2, f"بلاطة {slab_type}\n{n_bars}Φ{phi}/m\nh={h}cm", ha='center', fontweight='bold')
    ax.text(0.1, -0.5, SEAL, fontsize=8, color='blue')
    plt.axis('off')
    st.pyplot(fig)

# --- 3. الصفحة الثالثة: الجوائز الساقطة ---
def show_p3():
    st.header("📏 دراسة الجوائز الساقطة")
    bw = st.number_input("عرض الجائز bw (cm)", value=25)
    h = st.number_input("ارتفاع الجائز h (cm)", value=60)
    L = st.number_input("المجاز (m)", value=5.0)
    phi_main = st.selectbox("قطر الحديد الطولي", [14, 16, 18, 20], index=1)
    
    mu = (30 * L**2) / 8 # حمولة افتراضية
    as_req = (mu * 10**6) / (0.8 * st.session_state['fy'] * (h-5)*10)
    n_bars = max(2, int(np.ceil(as_req / (np.pi*phi_main**2/4))))

    fig, ax = plt.subplots(figsize=(4, 6))
    ax.add_patch(patches.Rectangle((0, 0), bw, h, fill=None, lw=3)) # المقطع
    ax.add_patch(patches.Rectangle((2, 2), bw-4, h-4, fill=None, edgecolor='green', label='الكانات')) # كانة
    # أسياخ سفلية
    for i in np.linspace(5, bw-5, n_bars):
        ax.add_patch(plt.Circle((i, 5), 1.5, color='red'))
    ax.text(bw/2, -10, f"التسليح: {n_bars}Φ{phi_main}\nالكانات: Φ8/20cm\n{SEAL}", ha='center', fontsize=9)
    plt.axis('off')
    st.pyplot(fig)

# --- 4. الصفحة الرابعة: الأعمدة ---
def show_p4():
    st.header("🏢 دراسة الأعمدة")
    a = st.number_input("بعد العمود a (cm)", value=50)
    b = st.number_input("بعد العمود b (cm)", value=30)
    pu = st.number_input("الحمولة Pu (kN)", value=1500.0)
    
    ag = a * b
    as_min = 0.01 * ag
    n_bars = max(4, int(np.ceil(as_min / (np.pi*16**2/400))))
    if n_bars % 2 != 0: n_bars += 1

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.add_patch(patches.Rectangle((0, 0), b, a, fill=None, lw=3))
    for i in np.linspace(5, a-5, n_bars//2):
        ax.add_patch(plt.Circle((5, i), 1.5, color='red'))
        ax.add_patch(plt.Circle((b-5, i), 1.5, color='red'))
    ax.text(b/2, -10, f"العمود: {int(n_bars)}Φ16\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- 5. الصفحة الخامسة: الهوردي ---
def show_p5():
    st.header("🧱 دراسة الهوردي والأعصاب")
    hb = st.selectbox("ارتفاع البلوك", [15, 20, 25])
    ts = st.number_input("بلاطة التغطية", value=7)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.add_patch(patches.Rectangle((0, 0), 40, hb, color='gray', alpha=0.3)) # بلوك
    ax.add_patch(patches.Rectangle((52, 0), 40, hb, color='gray', alpha=0.3)) # بلوك
    ax.add_patch(patches.Rectangle((40, 0), 12, hb+ts, fill=None, lw=2)) # عصب
    ax.add_patch(plt.Circle((44, 4), 1.5, color='red'))
    ax.add_patch(plt.Circle((48, 4), 1.5, color='red'))
    ax.text(46, hb+ts+2, f"عصب هوردي\n2Φ14 سفلي\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- 6. الصفحة السادسة: الجوائز المخفية ---
def show_p6():
    st.header("📏 الجوائز المخفية")
    bw = st.number_input("عرض الجائز المخفي (cm)", value=80)
    h = st.number_input("الارتفاع (نفس الهوردي) (cm)", value=27)
    
    fig, ax = plt.subplots(figsize=(10, 3))
    ax.add_patch(patches.Rectangle((0, 0), bw, h, fill=None, lw=3))
    for i in np.linspace(5, bw-5, 8):
        ax.add_patch(plt.Circle((i, 5), 1.5, color='red'))
    ax.text(bw/2, -8, f"جائز مخفي: 8Φ16 سفلي\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

# --- 7. الصفحة السابعة: الأساسات ---
def show_p7():
    st.header("🦶 دراسة الأساسات")
    type_f = st.selectbox("نوع الأساس", ["مفرد", "مشترك", "إجر بطة", "حصيرة"])
    L = st.number_input("طول الأساس (m)", value=2.0)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.add_patch(patches.Rectangle((0, 0), L, L, fill=None, lw=3))
    ax.add_patch(patches.Rectangle((L/2-0.2, L/2-0.1), 0.4, 0.2, color='gray')) # عمود
    for i in np.linspace(0.2, L-0.2, 8):
        ax.plot([i, i], [0.1, L-0.1], color='red', lw=1)
        ax.plot([0.1, L-0.1], [i, i], color='red', lw=1)
    ax.text(L/2, -0.3, f"أساس {type_f}\nتسليح: 8Φ14/m بالاتجاهين\n{SEAL}", ha='center')
    plt.axis('off')
    st.pyplot(fig)

if __name__ == "__main__":
    main()
