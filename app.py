import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Jawad Expert Engine", layout="wide")

class JawadMasterEngine:
    @staticmethod
    def solve_with_boundary_conditions(spans, loads, start_fixity, end_fixity):
        """
        محرك تحليل إنشائي يأخذ بعين الاعتبار نوع المساند الطرفية (وثاقة أو استناد بسيط)
        """
        n = len(spans)
        num_eq = n + 1
        A = np.zeros((num_eq, num_eq))
        B = np.zeros(num_eq)

        # بناء مصفوفة المعادلات (Modified Three-Moment Equation)
        for i in range(1, n):
            L1, L2 = spans[i-1], spans[i]
            w1, w2 = loads[i-1], loads[i]
            A[i, i-1] = L1
            A[i, i] = 2 * (L1 + L2)
            A[i, i+1] = L2
            B[i] = -(w1 * L1**3 / 4 + w2 * L2**3 / 4)

        # شرط المسند البداية
        if start_fixity == "وثاقة (Fixed)":
            A[0, 0], A[0, 1] = 2 * spans[0], spans[0]
            B[0] = -(loads[0] * spans[0]**3 / 4)
        else: # بسيط (Pinned)
            A[0, 0] = 1
            B[0] = 0

        # شرط المسند النهاية
        if end_fixity == "وثاقة (Fixed)":
            A[n, n-1], A[n, n] = spans[-1], 2 * spans[-1]
            B[n] = -(loads[-1] * spans[-1]**3 / 4)
        else: # بسيط (Pinned)
            A[n, n] = 1
            B[n] = 0

        moments = np.linalg.solve(A, B)
        return list(moments)

st.title("🏗️ محرك الجواد الاحترافي (شروط الاستناد المتغيرة)")

with st.sidebar:
    st.header("⚙️ إعدادات المساند")
    start_f = st.selectbox("المسند الأول (Start)", ["بسيط (Pinned)", "وثاقة (Fixed)"])
    end_f = st.selectbox("المسند الأخير (End)", ["بسيط (Pinned)", "وثاقة (Fixed)"])
    st.divider()
    n_spans = st.number_input("عدد الفتحات", 1, 5, 2)
    b, h = 300, 600

spans, loads = [], []
cols = st.columns(n_spans)
for i in range(n_spans):
    with cols[i]:
        L = st.number_input(f"طول الفتحة {i+1} (m)", value=5.0, key=f"L{i}")
        w = st.number_input(f"الحمل {i+1} (kN/m)", value=30.0, key=f"W{i}")
        spans.append(L)
        loads.append(w)

if st.button("🚀 تحليل إنشائي دقيق"):
    m_supports = JawadMasterEngine.solve_with_boundary_conditions(spans, loads, start_f, end_f)
    
    st.subheader("📊 مخرجات التحليل (العزوم عند المساند)")
    
    # عرض العزوم
    m_data = [{"المسند": i, "العزم (kNm)": round(abs(m), 2)} for i, m in enumerate(m_supports)]
    st.table(pd.DataFrame(m_data))

    

    # حساب وتسليح
    st.subheader("🏗️ تفاصيل التسليح بناءً على نوع المساند")
    for i in range(n_spans):
        m_max = max(abs(m_supports[i]), abs(m_supports[i+1]))
        # حساب تقريبي لعزم المنتصف بناءً على شروط الاستناد
        m_span = (loads[i] * spans[i]**2 / 8) - (abs(m_supports[i]) + abs(m_supports[i+1]))/2
        
        st.write(f"**الفتحة {i+1}:** العزم السالب الأكبر = {round(m_max,1)} | العزم الموجب = {round(abs(m_span),1)}")

st.markdown("---")
st.write("للتواصل والدعم الفني: **0998449697**")
