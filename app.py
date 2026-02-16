import math

class SyrianStructuralEngine:
    def __init__(self):
        # ثوابت الكود السوري
        self.gamma_c = 1.5   # عامل أمان الخرسانة
        self.gamma_s = 1.15  # عامل أمان الفولاذ
        self.phone_number = "0998449697" # رقم التواصل للختم

    def design_column(self, Pu, b, h, fcu, fy):
        """تصميم الأعمدة القصيرة المعرضة لضغط مركزي"""
        # حساب المقاومة التصميمية
        fcd = 0.85 * fcu / self.gamma_c
        fsd = fy / self.gamma_s
        
        # المساحة المطلوبة للحديد (مع مراعاة نسبة 0.8% كحد أدنى)
        # Pu بالنيوتن، الأبعاد بالملم
        As_required = (Pu - (0.40 * fcd * b * h)) / (0.67 * fsd - 0.40 * fcd)
        As_min = 0.008 * b * h
        
        final_As = max(As_required, As_min)
        return {"Element": "Column", "As": round(final_As, 2), "Status": "Success"}

    def design_beam(self, Mu, b, d, fcu, fy):
        """تصميم الجوائز على العطف - الطريقة الحدية"""
        fcd = 0.85 * fcu / self.gamma_c
        # حساب عمق المنطقة المضغوطة (a)
        a = d - math.sqrt(d**2 - (2 * Mu) / (0.85 * fcd * b))
        As = (0.85 * fcd * b * a) / (fy / self.gamma_s)
        
        return {"Element": "Beam", "As": round(As, 2), "Depth_a": round(a, 2)}

    def design_slab(self, w_u, L, fcu, fy, thickness):
        """تصميم بلاطة مصمتة (اتجاه واحد)"""
        # حساب العزم الأقصى M = w*L^2 / 8
        Mu = (w_u * L**2) / 8
        return self.design_beam(Mu, 1000, thickness - 20, fcu, fy)

    def print_stamp(self):
        print("\n" + "="*40)
        print("تمت الحسابات وفق الكود العربي السوري و ملحقاته")
        print(f"المهندس المصمم: [اسمك الشخصي]")
        print(f"للمراجعة الفنية: {self.phone_number}")
        print("="*40)

# --- مثال لتشغيل البرنامج ---
engine = SyrianStructuralEngine()

# 1. تصميم عمود (حمولة 2000 كيلو نيوتن)
col_result = engine.design_column(2000000, 300, 600, 25, 400)
print(col_result)

# 2. تصميم جائز (عزم 150 كيلو نيوتن.متر)
beam_result = engine.design_beam(150e6, 250, 550, 25, 400)
print(beam_result)

# طباعة الختم النهائي
engine.print_stamp()
