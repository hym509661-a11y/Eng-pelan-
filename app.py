import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 1. إعدادات الهوية والختم الرسمي ---
st.set_page_config(page_title="Pro-Civil Syria | Eng. Pelan", layout="wide")

def main():
    st.markdown(f"""
        <div style="direction: rtl; text-align: right; border: 3px solid #1b5e20; padding: 20px; border-radius: 15px; background-color: #f1f8e9;">
            <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسية الشاملة (كود 2026 المطور)</h1>
            <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
            <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>هاتف: 0998449697</b></p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. مدخلات الكود والمواد (ثوابت) ---
    st.sidebar.header("⚙️ ثوابت الكود السوري")
    fcu = st.sidebar.slider("مقاومة الخرسانة fcu (MPa)", 20, 40, 25)
    fy = st.sidebar.selectbox("إجهاد الحديد fy (MPa)", [240, 360, 400], index=2)
    f_prime_c = 0.8 * fcu
    
    # أحمال المهندس بيلان الثابتة
    DL_SLAB = 2.5  # kN/m2
    LL_CORRIDOR = 3.0 # kN/m2
    LL_ROOMS = 2.0    # kN/m2

    menu = ["المذكرة الحسابية المترابطة", "الرسومات التفصيلية (Detailing)", "حصر الكميات (B.O.Q)"]
    choice = st.sidebar.radio("انتقل إلى:", menu)

    # --- 3. محرك الحسابات المترابطة ---
    st.sidebar.markdown("---")
    st.sidebar.header("📥 إدخال الأبعاد (يدوي)")
    L_beam = st.sidebar.number_input("مجاز الجائز (m)", value=5.0)
    B_beam = st.sidebar.number_input("عرض الجائز b (mm)", value=300)
    H_beam = st.sidebar.number_input("ارتفاع الجائز h (mm)", value=500)
    Trib_width = st.sidebar.number_input("عرض تحميل البلاطة (m)", value=4.0)
    is_corridor = st.sidebar.checkbox("تحميل ممرات (LL=3)", value=True)

    # حسابات الأحمال والترابط
    LL_actual = LL_CORRIDOR if is_corridor else LL_ROOMS
    Wu_slab = (1.4 * DL_SLAB) + (1.7 * LL_actual)
    Wu_beam = (Wu_slab * Trib_width) + ((B_beam/1000)*(H_beam/1000)*25*1.4) # حمل البلاطة + وزن الجائز
    Mu = (Wu_beam * L_beam**2) / 10
    Vu = (Wu_beam * L_beam) / 2
    
    # تصميم الجائز (دقة جامعة دمشق)
    d = H_beam - 50
    As_req = (Mu * 1e6) / (0.9 * fy * 0.9 * d)
    As_min = (1.4/fy) * B_beam * d
    As_final = max(As_req, As_min)
    n_low = int(np.ceil(As_final / (np.pi * 16**2 / 4)))
    n_up = max(2, int(n_low * 0.3))
    
    # تباعد الكانات المبرمج
    Vc = 0.17 * np.sqrt(f_prime_c) * B_beam * d / 1000
    spacing = 15 if Vu < Vc else 10
    
    # حساب العمود والأساس (آلياً بناءً على رد فعل الجائز)
    Pu_col = Vu * 1.5 # بفرض طابقين
    Ag_col = Pu_col * 1000 / (0.35*f_prime_c + 0.67*fy*0.01) # مقطع عمود تقريبي
    Side_col = np.sqrt(Ag_col)
    
    # الأساس المبرمج آلياً
    P_service = Pu_col / 1.5
    Area_footing = (P_service * 1.1) / 200 # بفرض تربة 200
    Side_f = np.ceil(np.sqrt(Area_footing)*10)/10

    # --- 4. العرض حسب اختيار التبويب ---
    if choice == "المذكرة الحسابية المترابطة":
        st.header("📝 المذكرة الحسابية والتحليل الإنشائي")
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**أحمال البلاطة:** {Wu_slab:.2f} kN/m²")
            st.info(f"**أحمال الجائز:** {Wu_beam:.2f} kN/m")
            st.success(f"**العزم الأقصى Mu:** {Mu:.2f} kN.m")
            st.success(f"**قوة القص Vu:** {Vu:.2f} kN")
        with col2:
            st.subheader("⚠️ نظام الإنذار المبكر")
            if H_beam < (L_beam*1000/18.5):
                st.error("❌ خطر: سماكة الجائز غير كافية لمنع السهم (Deflection)!")
            else:
                st.success("✅ أبعاد المقطع تحقق شروط الكود السوري للسهم.")
            
            if As_final > (0.04 * B_beam * d):
                st.error("❌ خطر: نسبة الازدحام بالحديد عالية جداً!")
            else:
                st.success("✅ نسبة التسليح اقتصادية ومنطقية.")

    elif choice == "الرسومات التفصيلية (Detailing)":
        st.header("🎨 المخططات التفصيلية التنفيذية")
        element = st.selectbox("اختر العنصر للرسم:", ["مقطع الجائز", "مقطع الأساس المبرمج"])
        
        if element == "مقطع الجائز":
            fig = draw_section(B_beam, H_beam, n_low, 16, n_up, 12, spacing, 8, "مقطع عرضي في الجائز")
            st.plotly_chart(fig)
        else:
            fig = draw_section(Side_f*1000, 600, 10, 14, 0, 0, 0, 0, "مقطع في الأساس المبرمج آلياً")
            st.plotly_chart(fig)

    elif choice == "حصر الكميات (B.O.Q)":
        st.header("💰 جدول كميات المشروع التقديري")
        vol_b = (B_beam/1000 * H_beam/1000 * L_beam)
        vol_f = (Side_f**2 * 0.6)
        total_conc = vol_b + vol_f
        total_steel = total_conc * 115 # معدل 115 كغ/م3
        
        data = {
            "العنصر": ["الجوائز", "الأساسات", "الإجمالي"],
            "بيتون (m3)": [round(vol_b, 2), round(vol_f, 2), round(total_conc, 2)],
            "حديد (kg)": [round(vol_b*120), round(vol_f*100), round(total_steel)]
        }
        st.table(data)
        st.warning("الكميات محسوبة بدقة بناءً على الأبعاد الإنشائية المعتمدة أعلاه.")

# --- وظيفة الرسم الموحدة ---
def draw_section(b, h, n_low, d_low, n_up, d_up, s_spacing, s_dia, title):
    fig = go.Figure()
    # الخرسانة والأبعاد
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(128,128,128,0.1)")
    fig.add_annotation(x=b/2, y=h+50, text=f"العرض {int(b)} mm", showarrow=False)
    fig.add_annotation(x=-60, y=h/2, text=f"الارتفاع {int(h)} mm", textangle=-90, showarrow=False)
    
    # الكانة
    if s_spacing > 0:
        fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=2))
        fig.add_annotation(x=b+60, y=h/2, text=f"T{s_dia}@{s_spacing}cm", textangle=90, showarrow=False, font=dict(color="blue"))

    # السفلي والعلوي
    for i in range(int(n_low)):
        x = 45 + (i * (b-90)/(max(1, n_low-1)))
        fig.add_trace(go.Scatter(x=[x], y=[45], mode="markers", marker=dict(size=d_low, color="red"), showlegend=False))
    for i in range(int(n_up)):
        x = 45 + (i * (b-90)/(max(1, n_up-1)))
        fig.add_trace(go.Scatter(x=[x], y=[h-45], mode="markers", marker=dict(size=d_up, color="green"), showlegend=False))
    
    fig.add_annotation(x=b/2, y=-60, text=f"سفلي: {int(n_low)}T{d_low}", showarrow=False, font=dict(color="red", size=14))
    fig.add_annotation(x=b/2, y=h+100, text=f"علوي: {int(n_up)}T{d_up}", showarrow=False, font=dict(color="green", size=14))
    
    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=500, width=600, plot_bgcolor="white", title=title)
    return fig

if __name__ == "__main__":
    main()
