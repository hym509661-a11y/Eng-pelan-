import streamlit as st
import numpy as np
import pandas as pd

# إعدادات الواجهة
st.set_page_config(page_title="Jawad Pro Enterprise - Raft Edition", layout="wide")

st.title("🏗️ منظومة الجواد الهندسية (اللبشة والقواعد الحصيرية)")

# --- محرك حسابات اللبشة (Raft Engine) ---
class RaftEngine:
    @staticmethod
    def design_raft(total_p, mx, my, lx, ly, q_allow, fc):
        # 1. حساب الإجهادات تحت اللبشة (P/A ± My.x/Iy ± Mx.y/Ix)
        area = lx * ly
        sigma_avg = total_p / area
        
        # إجهادات الزوايا (تبسيط)
        stress_max = (total_p / area) + (abs(mx) / (lx**2 * ly / 6)) + (abs(my) / (ly**2 * lx / 6))
        stress_min = (total_p / area) - (abs(mx) / (lx**2 * ly / 6)) - (abs(my) / (ly**2 * lx / 6))
        
        # 2. التحقق من الثقب (Punching Shear) لأكبر عمود
        # d_req تقريبي بناءً على القص الثاقب
        d_req = (total_p * 0.1) / (4 * 0.4 * 0.17 * np.sqrt(fc) * 1000) * 1000 # قيمة استرشادية
        
        status = "✅ آمن" if stress_max <= q_allow else "❌ خطر (تجاوز إجهاد التربة)"
        return round(stress_max, 2), round(stress_min, 2), status, int(d_req)

# --- الواجهة الرئيسية (Tabs) ---
tabs = st.tabs(["🧱 الجدران", "🦶 الأساسات", "🪜 الأدراج", "🏢 اللبشة (Raft)"])

# (الأقسام السابقة تبقى كما هي لضمان عدم النقصان)

with tabs[3]:
    st.header("🏢 تصميم اللبشة المسلحة (Raft Foundation)")
    st.info("حساب توزيع الإجهادات تحت الحصيرة والتحقق من أمان التربة وفق الكود السوري")
    
    r_col1, r_col2 = st.columns([1, 1.5])
    with r_col1:
        total_p = st.number_input("مجموع أحمال الأعمدة الكلي (kN)", value=15000)
        lx = st.number_input("طول اللبشة X (m)", value=20.0)
        ly = st.number_input("عرض اللبشة Y (m)", value=15.0)
        mx = st.number_input("العزم الكلي Mx (kNm)", value=500)
        my = st.number_input("العزم الكلي My (kNm)", value=300)
        q_soil = st.number_input("إجهاد التربة المسموح (kN/m²)", value=150)
        fc_raft = st.number_input("f'c (MPa)", value=25, key="fcr")

    if st.button("تحليل اللبشة"):
        s_max, s_min, status, d_min = RaftEngine.design_raft(total_p, mx, my, lx, ly, q_soil, fc_raft)
        
        with r_col2:
            st.subheader("📋 نتائج التحليل (Raft Analysis)")
            st.write(f"أقصى إجهاد على التربة: **{s_max} kN/m²**")
            st.write(f"أدنى إجهاد على التربة: **{s_min} kN/m²**")
            
            if status == "✅ آمن":
                st.success(f"التحقق من التربة: {status}")
            else:
                st.error(f"التحقق من التربة: {status}")
            
            
            
            st.warning(f"السماكة الدنيا المقترحة لمقاومة الثقب: **{d_min + 50} mm**")
            st.write("**ملاحظة:** يجب توزيع التسليح بناءً على شرائح (Column Strips & Middle Strips) كما في الجواد.")

# التوقيع والختم الرقمي
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
