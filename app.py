import streamlit as st

# 1. تعريف البيانات الأساسية
ST_NAME = "بيلان مصطفى عبد الكريم"
ST_TEL = "0998449697"
ST_WORK = "المهندس المدني - دراسة - إشراف - تعهدات"

# 2. إعدادات الصفحة والواجهة
st.set_page_config(page_title="Pelan Office v95", layout="wide")
st.markdown(f"""
<style>
    .stApp {{ background-color: #0b1619; color: white; }}
    .report-box {{ background: white; color: black; padding: 25px; border-radius: 10px; direction: rtl; border-right: 12px solid #d4af37; }}
    .cad-box {{ background: #111; border: 2px solid #444; padding: 20px; border-radius: 10px; color: #50c878; text-align: center; }}
    .stamp {{ border: 4px double #d4af37; padding: 15px; width: 300px; text-align: center; background: #fff; color: #000; float: left; margin-top: 25px; }}
</style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية (المدخلات)
with st.sidebar:
    st.header("⚙️ خيارات التصميم")
    mode = st.selectbox("نوع العنصر:", ["جائز (Beam)", "بلاطة (Slab)", "أساس (Footing)", "عمود (Column)", "خزان (Tank)"])
    B = st.number_input("العرض B (cm):", 20, 500, 30)
    H = st.number_input("الارتفاع H (cm):", 10, 500, 60)
    st.divider()
    n_bot = st.number_input("عدد قضبان السفلي:", 2, 20, 4)
    phi_bot = st.selectbox("قطر السفلي (mm):", [12, 14, 16, 18, 20, 25], index=2)
    n_top = st.number_input("عدد قضبان العلوي/تعليق:", 2, 20, 2)
    phi_top = st.selectbox("قطر العلوي (mm):", [10, 12, 14, 16], index=1)
    phi_stir = st.selectbox("قطر الكانة (mm):", [8, 10, 12])

# 4. عرض النتائج والمذكرة
st.markdown(f"<h1 style='text-align:center; color:#d4af37;'>🏢 Pelan Professional Office - v95</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown("<div class='report-box'>", unsafe_allow_html=True)
    st.subheader("📑 المذكرة الحسابية والفرش")
    st.write(f"**نوع العنصر الإنشائي:** {mode}")
    st.write(f"**الأبعاد المعتمدة:** {B}x{H} cm")
    st.divider()
    st.write(f"✅ **التسليح السفلي (الرئيسي):** {n_bot} T {phi_bot}")
    st.write(f"✅ **التسليح العلوي (التعليق):** {n_top} T {phi_top}")
    st.write(f"✅ **الكانات:** Φ {phi_stir} @ 15cm")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='cad-box'>", unsafe_allow_html=True)
    st.subheader("🖋️ مخطط تفريد الحديد")
    
    # تبديل الصور بناءً على الاختيار
    if "جائز" in mode:
        
    elif "أساس" in mode:
        
    elif "عمود" in mode:
        
    elif "بلاطة" in mode:
        
    else:
        
    
    st.markdown(f"**توصيف أوتوكاد:** {n_bot}T{phi_bot} + {n_top}T{phi_top}")
    st.markdown("</div>", unsafe_allow_html=True)

    # الختم الرسمي مع الرقم
    st.markdown(f"""
    <div class='stamp'>
        <p style='margin:0; font-weight:bold;'>المهندس المدني</p>
        <p style='color:#d4af37; font-size:20px; font-weight:bold; margin:5px 0;'>{ST_NAME}</p>
        <p style='margin:0; font-size:13px;'>{ST_WORK}</p>
        <p style='margin:5px 0; font-weight:bold; color:#1a1a1a;'>TEL: {ST_TEL}</p>
        <hr style='border:1px solid #d4af37; margin:8px;'>
        <p style='font-size:10px;'>ختم الاعتماد الهندسي v95</p>
    </div>
    <div style='clear:both;'></div>
    """, unsafe_allow_html=True)

st.divider()
st.info("ملاحظة: هذه النسخة مصممة للعمل على الجوال بدون أخطاء مسافات.")
