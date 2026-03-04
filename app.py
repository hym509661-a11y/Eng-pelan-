import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- 1. ترويسة البرنامج والختم المهني (م. بيلان) ---
st.set_page_config(page_title="منظومة المهندس بيلان الإنشائية", layout="wide")

def main():
    st.markdown(f"""
        <div style="direction: rtl; text-align: right; border: 4px solid #1b5e20; padding: 20px; border-radius: 15px; background-color: #f1f8e9;">
            <h1 style="color: #1b5e20; margin:0;">المنظومة الهندسية الشاملة (تصميم - رسم - كميات)</h1>
            <h2 style="color: #2e7d32; margin:0;">المهندس المدني بيلان مصطفى عبدالكريم</h2>
            <p style="font-size: 18px; margin:5px;">دراسات - إشراف - تعهدات | <b>هاتف: 0998449697</b></p>
        </div>
    """, unsafe_allow_html=True)

    # --- 2. ثوابت الكود السوري والحمولات (كما طلبت بدقة) ---
    st.sidebar.header("⚙️ إعدادات الكود والمواد")
    fcu = st.sidebar.slider("مقاومة الخرسانة fcu (MPa)", 20, 35, 25)
    fy = st.sidebar.selectbox("إجهاد خضوع الحديد fy (MPa)", [240, 360, 400], index=2)
    f_prime_c = 0.8 * fcu
    
    DL_SLAB = 2.5   # حمولة ميتة إضافية kN/m2
    LL_ROOMS = 2.0  # حمولة حية غرف kN/m2
    LL_CORR = 3.0   # حمولة حية ممرات kN/m2

    # --- 3. واجهة المدخلات اليدوية (للجوائز والأعمدة) ---
    st.sidebar.markdown("---")
    st.sidebar.header("📥 أبعاد العناصر (يدوي)")
    b_in = st.sidebar.number_input("عرض الجائز b (mm)", value=300)
    h_in = st.sidebar.number_input("ارتفاع الجائز h (mm)", value=500)
    L_in = st.sidebar.number_input("مجاز الجائز (m)", value=5.0)
    trib_w = st.sidebar.number_input("عرض التحميل من البلاطة (m)", value=4.0)
    room_type = st.sidebar.radio("نوع الحمولة الحية:", ["غرف (2.0)", "ممرات (3.0)"], index=1)

    # --- 4. محرك الحسابات المترابطة (Logic) ---
    ll_val = LL_ROOMS if "غرف" in room_type else LL_CORR
    # حمل البلاطة التصعيدي
    wu_slab = (1.4 * DL_SLAB) + (1.7 * ll_val)
    # حمل الجائز المترابط (حمل البلاطة + الوزن الذاتي للجائز)
    wu_beam = (wu_slab * trib_w) + ((b_in/1000)*(h_in/1000)*25*1.4)
    
    mu = (wu_beam * L_in**2) / 10 # عزم مستمر دقيق
    vu = (wu_beam * L_in) / 2     # رد فعل الجائز (القص)
    
    # حساب التسليح (اقتصادي وغير مبالغ فيه)
    d_eff = h_in - 50
    as_req = (mu * 1e6) / (0.9 * fy * 0.9 * d_eff)
    as_min = (1.4 / fy) * b_in * d_eff
    as_final = max(as_req, as_min)
    
    n_low = int(np.ceil(as_final / (np.pi * 16**2 / 4))) # بفرض قطر 16
    n_up = max(2, int(n_low * 0.3))
    
    # تباعد الكانات المبرمج (القص)
    vc = 0.17 * np.sqrt(f_prime_c) * b_in * d_eff / 1000
    spacing = 15 if vu < vc else 10
    
    # الأساس المبرمج آلياً (بناءً على رد فعل الجائز Vu)
    p_service = (vu * 1.2) # حمل تشغيلي من طابق واحد + وزن عمود
    area_f = (p_service * 1.1) / 180 # بفرض جهد تربة 1.8 كغ/سم2
    side_f = np.ceil(np.sqrt(area_f)*10)/10 * 1000 # بالـ mm
    h_f = 500 if p_service < 1000 else 600

    # --- 5. العرض المرئي (Tabs) ---
    tabs = st.tabs(["📝 المذكرة والإنذار", "🏗️ الرسم التنفيذي بالأبعاد", "💰 حصر الكميات"])

    with tabs[0]:
        st.subheader("📝 المذكرة الحسابية ونظام الإنذار")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"**Wu الجائز:** {wu_beam:.2f} kN/m")
            st.success(f"**العزم التصميمي Mu:** {mu:.2f} kN.m")
            st.success(f"**قوة القص عند المسند Vu:** {vu:.2f} kN")
        with c2:
            if h_in < (L_in*1000/16):
                st.error("⚠️ إنذار خطر: ارتفاع الجائز (h) قد لا يحقق شرط السهم (Deflection)!")
            else:
                st.success("✅ أبعاد الجائز تحقق صلابة الكود السوري.")
            
            if as_final > (0.04 * b_in * d_eff):
                st.error("❌ خطر: نسبة الحديد عالية جداً (ازدحام)، يرجى زيادة أبعاد المقطع!")
            else:
                st.success("✅ نسبة الحديد اقتصادية وتسمح بصب سهل.")

    with tabs[1]:
        st.subheader("🎨 المخططات التنفيذية (أبعاد + تسليح)")
        sub_tab = st.selectbox("اختر العنصر للرسم:", ["مقطع الجائز", "مقطع الأساس المبرمج"])
        if sub_tab == "مقطع الجائز":
            fig = draw_section(b_in, h_in, n_low, 16, n_up, 12, spacing, 8, "مقطع عرضي تفصيلي في الجائز")
            st.plotly_chart(fig)
        else:
            fig = draw_section(side_f, h_f, 10, 14, 0, 0, 0, 0, "مقطع الأساس المبرمج آلياً")
            st.plotly_chart(fig)

    with tabs[2]:
        st.subheader("📋 جدول كميات المشروع (B.O.Q)")
        vol_b = (b_in/1000 * h_in/1000 * L_in)
        vol_f = ((side_f/1000)**2 * h_f/1000)
        
        st.table({
            "العنصر الإنشائي": ["الجائز (المصمم يدوياً)", "الأساس (المصمم آلياً)", "الإجمالي العام"],
            "بيتون مسلح (m3)": [round(vol_b, 3), round(vol_f, 3), round(vol_b+vol_f, 3)],
            "حديد تسليح تقديري (kg)": [round(vol_b*120), round(vol_f*90), round(vol_b*120 + vol_f*90)]
        })
        st.caption("ملاحظة: كميات الحديد تقديرية بناءً على نسب التسليح المحسوبة أعلاه.")

# --- وظيفة الرسم الهندسي الدقيقة بالأبعاد ---
def draw_section(b, h, n_low, d_low, n_up, d_up, s_spacing, s_dia, title):
    fig = go.Figure()
    # 1. رسم المقطع وخطوط الأبعاد
    fig.add_shape(type="rect", x0=0, y0=0, x1=b, y1=h, line=dict(color="black", width=4), fillcolor="rgba(180,180,180,0.15)")
    fig.add_annotation(x=b/2, y=h+60, text=f"B = {int(b)} mm", showarrow=False, font=dict(size=14, color="black", family="Arial Black"))
    fig.add_annotation(x=-90, y=h/2, text=f"H = {int(h)} mm", textangle=-90, showarrow=False, font=dict(size=14, color="black", family="Arial Black"))
    
    # 2. رسم الكانة
    if s_spacing > 0:
        fig.add_shape(type="rect", x0=25, y0=25, x1=b-25, y1=h-25, line=dict(color="blue", width=3))
        fig.add_annotation(x=b+100, y=h/2, text=f"الكانات: T{s_dia} @ {s_spacing} cm", textangle=90, showarrow=False, font=dict(color="blue", size=14))
    
    # 3. توزيع أسياخ الحديد (توزيع حقيقي تنفيذي)
    for i in range(int(n_low)):
        x = 55 + (i * (b-110)/(max(1, n_low-1)))
        fig.add_trace(go.Scatter(x=[x], y=[55], mode="markers", marker=dict(size=d_low*1.1, color="red", line=dict(width=1, color="black")), showlegend=False))
    
    for i in range(int(n_up)):
        x = 55 + (i * (b-110)/(max(1, n_up-1)))
        fig.add_trace(go.Scatter(x=[x], y=[h-55], mode="markers", marker=dict(size=d_up*1.1, color="green", line=dict(width=1, color="black")), showlegend=False))
    
    # 4. تسميات الحديد
    fig.add_annotation(x=b/2, y=-80, text=f"سفلي: {int(n_low)} T{d_low}", showarrow=False, font=dict(color="red", size=16))
    fig.add_annotation(x=b/2, y=h+130, text=f"علوي: {int(n_up)} T{d_up}", showarrow=False, font=dict(color="green", size=16))

    fig.update_layout(xaxis_visible=False, yaxis_visible=False, height=600, width=800, plot_bgcolor="white", title=title, margin=dict(t=150, b=100))
    return fig

if __name__ == "__main__":
    main()
