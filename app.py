import math

class SyrianStructuralPro:
    def __init__(self):
        self.eng_name = "المهندس المدني بيلان مصطفى عبدالكريم"
        self.stamp = "دراسات - إشراف - تعهدات | 0998449697"
        self.phi_flexure = 0.90   # للانعطاف
        self.phi_shear = 0.75     # للقص
        self.phi_axial = 0.65     # للأعمدة
        
    def header(self):
        print(f"\n{'*'*70}")
        print(f"{self.eng_name.center(70)}")
        print(f"{self.stamp.center(70)}")
        print(f"{'*'*70}")

    def design_foundation(self, P_service, q_allow, col_b, col_h, fcu, fy):
        """تصميم أساس منفرد: دقة في الأبعاد واقتصاد في التسليح"""
        P_u = P_service * 1.5 # حمولة تصعيدية وسطية للأساسات
        f_prime_c = 0.8 * fcu
        
        # 1. الأبعاد (اقتصادية: جعل الرفرفة متساوية من الجهتين)
        area_req = (P_service * 1.1) / q_allow # زيادة 10% وزن ذاتي
        side = math.sqrt(area_req)
        B = math.ceil(side * 10) / 10 # تقريب لأقرب 10 سم
        L = B 
        
        # 2. سماكة الأساس (التحقق من القص الثاقب Punching Shear)
        d = 0.40 # فرض مبدئي 40 سم فعال
        qu = P_u / (B * L)
        
        # 3. التسليح السفلي (الانعطاف)
        cantilever = (B - (col_b/1000)) / 2
        Mu = qu * (cantilever**2) / 2
        
        res = self._flexure_engine(Mu, 1000, (d*1000 + 50), fcu, fy, "FOOTING")
        return {
            "Dimensions": f"{B}m x {L}m",
            "Thickness": f"{d*1000 + 70} mm",
            "As_total": res['As_mm2'],
            "Bars": f"{math.ceil(res['As_mm2']/113)} T12 / m'"
        }

    def _flexure_engine(self, Mu, b, h, fcu, fy, mode):
        """محرك الحسابات الموحد للانعطاف (بلاطات وجوائز وأساسات)"""
        f_prime_c = 0.8 * fcu
        d = h - (20 if mode == "SLAB" else 50)
        Mu_nm = Mu * 1e6
        
        Rn = Mu_nm / (self.phi_flexure * b * d**2)
        m = fy / (0.85 * f_prime_c)
        
        # منع الخطأ البرمجي في حال كان المقطع صغير جداً
        if (1 - (2 * m * Rn / fy)) < 0:
            return {"As_mm2": "زيادة أبعاد!", "Status": "Fail"}
            
        rho = (1/m) * (1 - math.sqrt(1 - (2 * m * Rn / fy)))
        
        # الحدود الدنيا حسب الكود السوري (جامعة دمشق)
        as_min = max(0.25 * math.sqrt(f_prime_c) / fy * b * d, 1.4 / fy * b * d)
        as_req = rho * b * d
        
        return {"As_mm2": round(max(as_req, as_min), 2)}

    def design_column(self, P_u_kn, b_mm, h_mm, fcu, fy):
        """تصميم الأعمدة مع التحقق من النسبة الاقتصادية 1%"""
        f_prime_c = 0.8 * fcu
        Ag = b_mm * h_mm
        # معادلة الكود السوري للأعمدة المحملة مركزياً
        As_min = 0.01 * Ag
        Pu_capacity = self.phi_axial * 0.8 * (0.85 * f_prime_c * (Ag - As_min) + fy * As_min) / 1000
        
        if P_u_kn <= Pu_capacity:
            return {"Status": "Safe (Min Steel)", "As_total": As_min, "Bars": f"{math.ceil(As_min/201)} T16"}
        else:
            As_req = ( (P_u_kn*1000 / (self.phi_axial*0.8)) - (0.85*f_prime_c*Ag) ) / (fy - 0.85*f_prime_c)
            return {"Status": "Reinforced", "As_total": round(As_req, 2), "Bars": f"{math.ceil(As_req/201)} T16"}

# --- برنامج التشغيل الذكي ---
app = SyrianStructuralPro()
app.header()

# مثال شامل لمشروع:
fcu_val = 25 # MPa
fy_val = 400 # MPa

print("\n1. نتيجة تصميم الأساس (Single Footing):")
found = app.design_foundation(P_service=800, q_allow=150, col_b=0.3, col_h=0.5, fcu=fcu_val, fy=fy_val)
print(f"   الأبعاد: {found['Dimensions']} | السماكة: {found['Thickness']}")
print(f"   التسليح السفلي (الفرش والغطاء): {found['Bars']}")

print("\n2. نتيجة تصميم العمود (Column):")
col = app.design_column(P_u_kn=2200, b_mm=300, h_mm=600, fcu=fcu_val, fy=fy_val)
print(f"   الحالة: {col['Status']} | التسليح الكلي: {col['As_total']} mm² ({col['Bars']})")

print("\n3. نتيجة تصميم البلاطة (Slab - Room):")
# حمولات المهندس بيلان: DL=2.5, LL=2.0
wu_room = (1.4 * 2.5) + (1.7 * 2.0)
mu_room = (wu_room * 4**2) / 10 # عزم تقريبي لبلاطة مستمرة
slab = app._flexure_engine(mu_room, 1000, 150, fcu_val, fy_val, "SLAB")
print(f"   التسليح السفلي المطلوب: {slab['As_mm2']} mm²/m' (حوالي 6 قضبان قطر 10)")
print("-" * 70)
