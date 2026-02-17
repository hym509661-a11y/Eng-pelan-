import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Jawad Frame Pro", layout="wide")

class FrameEngine:
    @staticmethod
    def calculate_distribution_factors(l_beam, i_beam, h_col_top, i_col_top, h_col_bot, i_col_bot):
        # حساب الجساءة K = I/L
        k_beam = i_beam / l_beam
        k_col_t = i_col_top / h_col_top
        k_col_b = i_col_bot / h_col_bot
        
        sum_k = k_beam + k_col_t + k_col_b
        
        # معاملات التوزيع (Distribution Factors) - جوهر التحليل الإطاري
        df_beam = k_beam / sum_k
        df_col_t = k_col_t / sum_k
        df_col_b = k_col_b / sum_k
        
        return df_beam, df_col_t, df_col_b

st.title("🏗️ وحدة تحليل الإطارات (الجوائز المترابطة مع الأعمدة)")
st.info("التحليل يعتمد على انتقال العزوم بين الجائز والأعمدة بناءً على جساءة كل عنصر (Hardcore Engineering)")

with st.sidebar:
    st.header("📏 أبعاد الجائز (Beam)")
    l_b = st.number_input("طول الجائز (m)", value=6.0)
    b_b = st.number_input("عرض الجائز (mm)", value=300)
    h_b = st.number_input("ارتفاع الجائز (mm)", value=600)
    
    st.header("🏢 أبعاد الأعمدة (Columns)")
    b_c = st.number_input("عرض العمود (mm)", value=400)
    h_c = st.number_input("عمق العمود (mm)", value=400)
    h_stack = st.number_input("ارتفاع الطابق (m)", value=3.0)

# حساب عزوم العطالة (Moment of Inertia)
i_beam = (b_b * h_b**3) / 12
i_col = (b_c * h_c**3) / 12

# حساب معاملات التوزيع عند العقدة
df_b, df_ct, df_cb = FrameEngine.calculate_distribution_factors(l_b, i_beam, h_stack, i_col, h_stack, i_col)

st.subheader("📊 معاملات توزيع العزوم عند العقدة (Joint D.F)")
c1, c2, c3 = st.columns(3)
c1.metric("للحمال (Beam)", f"{round(df_b, 3)}")
c2.metric("للعمود العلوي", f"{round(df_ct, 3)}")
c3.metric("للعمود السفلي", f"{round(df_cb, 3)}")

# التحليل الإنشائي (Moment Distribution)
w_total = st.number_input("الحمل الموزع على الجائز (kN/m)", value=40.0)
fem = (w_total * l_b**2) / 12 # عزم الوثاقة الابتدائي

m_beam = fem * (1 - df_b) # العزم الذي سيبقى في الجائز بعد التوزيع
m_col_total = fem * df_b  # العزم الذي سينتقل للأعمدة

st.divider()
st.subheader("📉 نتائج العزوم المترابطة (Frame Moments)")



res_col1, res_col2 = st.columns(2)
with res_col1:
    st.write(f"**عزم الوثاقة الابتدائي (FEM):** {round(fem, 2)} kNm")
    st.write(f"**العزم النهائي في الجائز عند المسند:** {round(m_beam, 2)} kNm")
    st.success(f"**العزم المنقول للأعمدة:** {round(m_col_total, 2)} kNm")

with res_col2:
    st.info("توزيع العزم على الأعمدة:")
    st.write(f"- العمود العلوي: {round(m_col_total * (df_ct/(df_ct+df_cb)), 2)} kNm")
    st.write(f"- العمود السفلي: {round(m_col_total * (df_cb/(df_ct+df_cb)), 2)} kNm")

st.divider()
st.subheader("🏗️ تصميم تسليح العقدة (Joint Detailing)")
st.write("بناءً على العزوم أعلاه، يجب تأمين طول تشريك كافٍ لحديد الجائز داخل العمود.")



# التذييل المطلوب
st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
