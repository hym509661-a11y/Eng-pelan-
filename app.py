import pandas as pd
import streamlit as st

class PelanEngine:
    def __init__(self):
        self.project_data = []

    def add_column(self, name, load_kn, fc, fy):
        # حساب مقطع العمود التقريبي (P = 0.35*fc*Ac + 0.67*fy*As)
        # بفرض نسبة تسليح 1%
        ac_req = (load_kn * 1000) / (0.35 * fc + 0.67 * fy * 0.01)
        side = (ac_req)**0.5
        self.project_data.append({
            'Element': 'Column',
            'ID': name,
            'Result': f"{round(side/10)*10}x{round(side/10)*10} mm",
            'Steel': f"{round(ac_req*0.01)} mm²"
        })

    def add_beam(self, name, mu_knm, b, d, fc, fy):
        # كود التصميم الذي كتبناه سابقاً
        phi = 0.9
        rn = (mu_knm * 10**6) / (phi * b * d**2)
        m = fy / (0.85 * fc)
        rho = (1/m) * (1 - (1 - (2*m*rn/fy))**0.5)
        as_req = rho * b * d
        self.project_data.append({
            'Element': 'Beam',
            'ID': name,
            'Result': f"{b}x{int(d+40)} mm",
            'Steel': f"{round(as_req)} mm²"
        })

# واجهة الاستخدام
st.title("Pelan Structural Workstation v1.0")

engine = PelanEngine()

tab1, tab2, tab3 = st.tabs(["الأعمدة", "الجوائز", "الأساسات"])

with tab1:
    col_name = st.text_input("اسم العمود", "C1")
    load = st.number_input("الحمولة التصاعدية (kN)", value=1200)
    if st.button("إضافة العمود للمشروع"):
        engine.add_column(col_name, load, 20, 400)
        st.success(f"تمت إضافة {col_name}")

with tab2:
    beam_name = st.text_input("اسم الجائز", "B1")
    mu = st.number_input("العزم (kN.m)", value=180)
    if st.button("إضافة الجائز للمشروع"):
        engine.add_beam(beam_name, mu, 200, 460, 20, 400)
        st.success(f"تمت إضافة {beam_name}")

# عرض النتائج النهائية للتصدير
if len(engine.project_data) > 0:
    df = pd.DataFrame(engine.project_data)
    st.table(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("تصدير ملف المشروع المتكامل", csv, "project_pelan.csv")
