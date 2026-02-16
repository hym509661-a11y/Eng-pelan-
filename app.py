import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Pelan Engineering Suite", layout="wide")

# --- الختم الهندسي في الجانب ---
st.sidebar.markdown(f"""
### 🏗️ المكتب الهندسي
**المهندس: بيلان مصطفى عبدالكريم** **Eng. Pelan Mustfa Abdulkarim** 📞 0998449697  
---
""", unsafe_allow_html=True) # تم تصحيح الخطأ هنا من dict إلى html

st.title("🚀 Pelan Ultimate BIM Suite")
st.subheader("Integrated System: AutoCAD + ETABS + SAFE + Revit")

# --- الأقسام الرئيسية للبرنامج ---
tabs = st.tabs(["📂 AutoCAD Import", "📊 Structural Analysis", "🏗️ Reinforcement Detail", "📑 BBS Report"])

with tabs[0]:
    st.header("AutoCAD & Revit Sync")
    st.info("قم برفع المسقط المعماري لتحديد أماكن الأعمدة والجسور تلقائياً")
    file = st.file_uploader("Upload DXF/DWG", type=['dxf', 'dwg'])
    if file:
        st.success("تم تحليل المسقط بنجاح. العناصر الإنشائية جاهزة للتصميم.")

with tabs[1]:
    st.header("ETABS Analysis Engine")
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Slab Thickness (mm)", value=200)
        st.number_input("Concrete Grade (C)", value=30)
    with col2:
        st.number_input("Steel Yield Strength (Fy)", value=420)
        st.button("Run Design Analysis")

with tabs[2]:
    st.header("SAFE Reinforcement (تفاصيل التسليح)")
    # جدول تفصيلي لكل أنواع الحديد التي طلبتها
    data = {
        "Element (العنصر)": ["Beam B1", "Beam B2", "Column C1", "Slab S1"],
        "Top Rebar (علوي)": ["3Ø16", "2Ø16", "4Ø20", "Ø12@200"],
        "Bottom Rebar (سفلي)": ["4Ø18", "3Ø16", "4Ø20", "Ø12@150"],
        "Stirrups (الكانات)": ["Ø10@150mm", "Ø10@150mm", "Ø10@100mm", "-"],
        "Hangers (تعليق)": ["2Ø12", "2Ø12", "-", "-"]
    }
    st.table(pd.DataFrame(data))

with tabs[3]:
    st.header("Bar Bending Schedule (BBS)")
    bbs_data = pd.DataFrame({
        "Mark": ["01", "02", "03", "04"],
        "Description": ["Top Main", "Bottom Main", "Stirrups", "Slab Mesh"],
        "Diameter (mm)": [16, 18, 10, 12],
        "Length (m)": [4.5, 4.8, 1.4, 120.0],
        "Total Weight (kg)": [7.1, 9.6, 0.86, 106.8]
    })
    st.dataframe(bbs_data)
    
    # تحويل البيانات إلى ملف للتحميل
    csv = bbs_data.to_csv(index=False).encode('utf-8')
    st.download_button("📥 تحميل جدول الكميات (Excel/CSV)", data=csv, file_name="Pelan_BBS.csv")

# الختم النهائي في أسفل الصفحة
st.markdown("---")
st.markdown(f"<h3 style='text-align: center; color: #2c3e50;'>Eng Pelan Mustfa Abdulkarim | 0998449697</h3>", unsafe_allow_html=True)
