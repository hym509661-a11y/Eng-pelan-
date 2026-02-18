import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# إعدادات الختم الرسمي [2026-02-18]
SEAL = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات 0998449697"

def main():
    st.sidebar.title("نظام التصميم الإنشائي المتكامل")
    st.sidebar.info(SEAL)
    
    menu = ["1. المدخلات العامة", "2. البلاطات المصمتة", "3. الجوائز الساقطة", "4. الأعمدة", "5. الهوردي والآجر", "6. الجوائز المخفية", "7. الأساسات"]
    choice = st.sidebar.selectbox("القائمة الرئيسية", menu)

    if choice == "1. المدخلات العامة":
        show_page_1()
    elif choice == "2. البلاطات المصمتة":
        show_page_2()

# --- الصفحة الأولى: المدخلات العامة ---
def show_page_1():
    st.header("📋 المدخلات العامة للمشروع")
    st.markdown(f"**إشراف: {SEAL}**")
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("💡 خصائص المواد")
        st.session_state['fcu'] = st.number_input("إجهاد الخرسانة المميز (fcu) - MPa", value=25.0)
        st.session_state['fy'] = st.number_input("إجهاد خضوع الحديد (fy) - MPa", value=400.0)
    with col2:
        st.subheader("⚖️ الأحمال")
        st.session_state['LL'] = st.number_input("الحمولة الحية (LL) - kN/m²", value=2.0)
        st.session_state['Cover'] = st.number_input("حمولة التغطية (Cover) - kN/m²", value=1.5)
    st.success("تم حفظ المدخلات العامة بنجاح. يمكنك الانتقال لصفحات الدراسة.")

# --- الصفحة الثانية: البلاطات المصمتة ---
def show_page_2():
    st.header("🏗️ دراسة البلاطات المصمتة (Solid Slabs)")
    st.markdown(f"**{SEAL}**")
    st.divider()

    # 1. المدخلات التفصيلية
    col_dim1, col_dim2 = st.columns(2)
    with col_dim1:
        Ly = st.number_input("الطول الأطول للفتحة (Ly) - m", value=5.0)
        Lx = st.number_input("الطول الأقصر للفتحة (Lx) - m", value=4.0)
    with col_dim2:
        phi_main = st.selectbox("قطر الحديد الرئيسي (mm)", [8, 10, 12, 14], index=1)
        phi_add = st.selectbox("قطر الحديد الإضافي (mm)", [8, 10, 12], index=1)

    # 2. منطق الكود في اختيار النوع والسماكة
    r = Ly / Lx
    is_one_way = r > 2
    slab_type = "اتجاه واحد (One-Way)" if is_one_way else "اتجاهين (Two-Way)"
    
    # حساب السماكة حسب الكود (ضبط السهم)
    h_min = (Lx * 100) / (30 if is_one_way else 35)
    h = st.number_input(f"السماكة المقترحة (الدنيا {h_min:.1f} cm) - اختر السماكة:", value=float(np.ceil(h_min)))

    # 3. الحسابات الإنشائية (العزوم والقص وردود الأفعال)
    fcu = st.session_state.get('fcu', 25)
    fy = st.session_state.get('fy', 400)
    w_u = 1.4 * (h/100 * 25 + st.session_state.get('Cover', 1.5)) + 1.6 * st.session_state.get('LL', 2.0)
    
    # العزوم (مثال بسيط للتوضيح)
    if is_one_way:
        Mu = (w_u * Lx**2) / 8
        As_req = (Mu * 10**6) / (0.8 * fy * (h-2)*10)
    else:
        alpha = (r**4) / (1 + r**4)
        Mu = alpha * (w_u * Lx**2) / 8
        As_req = (Mu * 10**6) / (0.8 * fy * (h-2)*10)
    
    n_bars = max(5, int(np.ceil(As_req / (np.pi * phi_main**2 / 4))))

    # 4. الرسوم الهندسية الدقيقة
    st.subheader("📊 المخطط الإنشائي وتوزيع الحديد")
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # رسم البلاطة
    rect = patches.Rectangle((0, 0), Lx, Ly, linewidth=3, edgecolor='black', facecolor='#f0f0f0', label='البلاطة')
    ax.add_patch(rect)
    
    # رسم حديد التسليح السفلي (خطوط متواصلة)
    spacing = Lx / n_bars
    for i in range(1, n_bars):
        ax.plot([i*spacing, i*spacing], [0.1, Ly-0.1], color='red', lw=1.2)
    
    # رسم الحديد الإضافي عند المساند (خطوط متقطعة)
    ax.plot([0.1, Lx-0.1], [Ly-0.3, Ly-0.3], color='blue', linestyle='--', lw=2, label='إضافي علوي')

    # كتابة البيانات والختم على الرسم
    ax.text(Lx/2, Ly/2, f"بلاطة {slab_type}\nh = {h} cm\n{n_bars}Φ{phi_main}/m'", ha='center', fontsize=12, fontweight='bold')
    ax.text(0.1, -0.6, SEAL, fontsize=10, color='darkblue', fontweight='bold')
    
    ax.set_xlim(-1, Lx+1)
    ax.set_ylim(-1, Ly+1)
    ax.axis('off')
    st.pyplot(fig)

    # جدول النتائج
    st.table({
        "البيان": ["نوع البلاطة", "الحمولة التصعيدية Wu", "العزم التصميمي Mu", "التسليح الرئيسي", "التسليح العرضي/التعليق"],
        "القيمة": [slab_type, f"{w_u:.2f} kN/m²", f"{Mu:.2f} kN.m", f"{n_bars} Φ {phi_main} / m'", "5 Φ 8 / m'"]
    })

if __name__ == "__main__":
    main()
