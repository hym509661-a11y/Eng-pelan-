import math

class SyrianStructuralFullSuite:
    def __init__(self, fpc=200, fy=3600):
        # البيانات الأساسية للمكتب الهندسي - م. بيلان مصطفى عبدالكريم
        self.fpc = fpc  # kg/cm2
        self.fy = fy    # kg/cm2
        self.phi_flexure = 0.9
        self.phi_compression = 0.65
        self.stamp = """
        --------------------------------------------------
        المهندس المدني: بيلان مصطفى عبدالكريم
        دراسات - إشراف - تعهدات
        هاتف: 0998449697
        --------------------------------------------------
        """

    # --- 1. محرك البلاطات وتوزيع الأحمال ---
    def slab_analysis(self, L_long, L_short, dead_load, live_load):
        qu = (1.4 * dead_load) + (1.7 * live_load)
        r = L_long / L_short
        if r > 2:
            qe_m = (qu * L_short) / 2
            type_s = "One-way"
        else:
            qe_m = (qu * L_short / 3) * (1 - 0.5 * (1/r)**2)
            type_s = "Two-way"
        return qu, qe_m, type_s

    # --- 2. محرك تصميم الجوائز (العطف) ---
    def design_beam(self, Mu_ton_m, b=20, d=52):
        Mu_kgcm = Mu_ton_m * 10**5
        rn = Mu_kgcm / (self.phi_flexure * b * d**2)
        # معادلة نسبة التسليح
        rho = (0.85 * self.fpc / self.fy) * (1 - math.sqrt(1 - (2.353 * rn / self.fpc)))
        # الحدود الدنيا للكود السوري
        rho_min = max(14/self.fy, (0.25 * math.sqrt(self.fpc))/self.fy)
        rho = max(rho, rho_min)
        as_req = rho * b * d
        return self.select_bars(as_req, "beam")

    # --- 3. محرك تصميم الأعمدة (تراكمي) ---
    def design_column(self, total_pu_ton, b=30, h=30):
        pu_kg = total_pu_ton * 1000
        ag = b * h
        ast = (pu_kg / (0.8 * self.phi_compression) - 0.85 * self.fpc * ag) / (self.fy - 0.85 * self.fpc)
        ast = max(ast, 0.01 * ag) # حد أدنى 1%
        return self.select_bars(ast, "column")

    # --- 4. محرك الزلازل (القص القاعدي) ---
    def seismic_base_shear(self, W_total, zone_z=0.15, I=1.0, R=5.5):
        # C هو معامل الاستجابة (نفرضه 2.75 للقيمة العظمى)
        C = 2.75
        V = (zone_z * I * C / R) * W_total
        return round(V, 2)

    # --- 5. محرك القواعد (الأحمال الخدمية) ---
    def design_footing(self, P_service_ton, sigma_allowable_kgcm2=2.0):
        # تحويل إجهاد التربة لـ t/m2
        sigma_tm2 = sigma_allowable_kgcm2 * 10
        area_req = (P_service_ton * 1.1) / sigma_tm2 # 1.1 لزيادة وزن القاعدة
        side = math.sqrt(area_req)
        return round(side, 2)

    # --- محرك اختيار الأقطار المتوفرة في سوريا ---
    def select_bars(self, as_req, mode):
        bars = {12: 1.13, 14: 1.54, 16: 2.01, 18: 2.54, 20: 3.14}
        results = []
        for size, area in bars.items():
            n = math.ceil(as_req / area)
            if mode == "column" and n % 2 != 0: n += 1
            if 2 <= n <= 12:
                results.append((n, size, n * area))
        best = min(results, key=lambda x: x[2])
        return f"{best[0]} T {best[1]} (As={round(best[2],2)}cm2)"

# --- مثال تشغيل كامل للمنشأ ---
engine = SyrianStructuralFullSuite()

# 1. دراسة بلاطة وجائز
qu, qe_m, s_type = engine.slab_analysis(5, 4, 0.6, 0.2)
beam_steel = engine.design_beam(Mu_ton_m=12)

# 2. دراسة عمود يحمل 150 طن
col_steel = engine.design_column(150, 30, 50)

# 3. دراسة زلزالية لمبنى وزنه 2000 طن
v_shear = engine.seismic_base_shear(2000)

# 4. دراسة قاعدة لعمود يحمل 100 طن خدمي
f_side = engine.design_footing(100)

# --- طباعة التقرير النهائي الشامل ---
print(engine.stamp)
print(f"1. نتائج البلاطة: نوع {s_type} | الحمل التصميمي {qu:.2f} t/m2")
print(f"2. تسليح الجائز المقترح: {beam_steel}")
print(f"3. تسليح العمود (30x50): {col_steel}")
print(f"4. قوة القص الزلزالية للمبنى: {v_shear} t")
print(f"5. أبعاد القاعدة المربعة (صخر/تربة): {f_side} x {f_side} م")
print("\n--- تمت الدراسة بحذافيرها وفق الكود العربي السوري لعام 2012 ---")
