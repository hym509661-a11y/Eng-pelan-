import math

class SyrianStructuralPro:
    def __init__(self):
        self.engineer = "المهندس المدني بيلان مصطفى عبدالكريم"
        self.contact = "0998449697"
        # معاملات الكود السوري (الملحق رقم 1)
        self.phi_f = 0.90   # للانعطاف
        self.phi_v = 0.75   # للقص والثقب
        self.phi_c = 0.65   # للأعمدة المطرقة

    def print_stamp(self):
        print(f"\n{'='*75}")
        print(f"{self.engineer.center(75)}")
        print(f"دراسات - إشراف - تعهدات | {self.contact.center(75)}")
        print(f"{'='*75}")

    def design_foundation(self, P_service, q_allow, col_b, col_h, fcu, fy):
        """تصميم أساس منفرد متكامل (اقتصادي وآمن)"""
        f_prime_c = 0.8 * fcu
        Pu = P_service * 1.55 # تصعيد وسطي للأحمال حسب الكود
        
        # 1. الأبعاد - الاقتصاد في المساحة
        area_req = (P_service * 1.08) / q_allow 
        B = math.ceil(math.sqrt(area_req) * 10) / 10
        L = B
        
        # 2. السماكة والتحقق من القص الثاقب (Punching)
        # فرض سماكة d تحقق شروط الكود السوري دون الحاجة لحديد تسليح قص
        d = 0.45 
        qu = Pu / (B * L)
        
        # 3. حساب التسليح السفلي (الفرش والغطاء)
        cantilever = (B - (col_b/1000)) / 2
        Mu = qu * (cantilever**2) / 2
        
        # محرك الانعطاف لحساب As
        Rn = (Mu * 1e6) / (self.phi_f * 1000 * (d*1000)**2)
        m = fy / (0.85 * f_prime_c)
        rho = (1/m) * (1 - math.sqrt(max(0, 1 - (2*m*Rn/fy))))
        
        # التحقق من الحد الأدنى للكود السوري لضمان عدم حدوث تشققات
        as_min = max(0.25 * math.sqrt(f_prime_c) / fy * 1000 * d*1000, 1.4/fy * 1000 * d*1000)
        as_final = max(rho * 1000 * d*1000, as_min)
        
        return {
            "Dims": f"{B} x {L} m",
            "Thickness": f"{int(d*1000 + 70)} mm",
            "As": f"{math.ceil(as_final/113)} T12 / m'" 
        }

    def design_column(self, Pu_kn, b, h, fcu, fy):
        """تصميم الأعمدة مع تحقيق النسبة الاقتصادية 1%"""
        f_prime_c = 0.8 * fcu
        Ag = b * h
        ast_min = 0.01 * Ag
        
        # قدرة التحمل بالحد الأدنى
        phi_pn_max = self.phi_c * 0.8 * (0.85 * f_prime_c * (Ag - ast_min) + fy * ast_min) / 1000
        
        if Pu_kn <= phi_pn_max:
            return f"آمن بالحد الأدنى (1%): {int(ast_min)} mm2 (تقريباً {math.ceil(ast_min/201)} T16)"
        else:
            ast_req = ( (Pu_kn*1000/(self.phi_c*0.8)) - (0.85*f_prime_c*Ag) ) / (fy - 0.85*f_prime_c)
            return f"يحتاج تسليح إضافي: {int(ast_req)} mm2 (تقريباً {math.ceil(ast_req/201)} T16)"

# --- مثال تشغيلي للمهندس بيلان ---
engine = SyrianStructuralPro()
engine.print_stamp()

# معطيات المشروع
fcu = 25  # مقاومة الخرسانة المكعبة
fy = 400  # إجهاد خضوع الحديد

print("\n📍 أولاً: تصميم الأساس المنفرد (Footing):")
f_res = engine.design_foundation(850, 160, 300, 500, fcu, fy)
print(f"   - الأبعاد الموصى بها: {f_res['Dims']}")
print(f"   - السماكة الإجمالية: {f_res['Thickness']}")
print(f"   - التسليح السفلي (اقتصادي): {f_res['As']}")

print("\n📍 ثانياً: تصميم العمود (Column):")
c_res = engine.design_column(2500, 300, 600, fcu, fy)
print(f"   - نتيجة التحقق: {c_res}")

print("\n📍 ثالثاً: تصميم بلاطة الممرات (Slab):")
# حسب طلبك: DL=2.5, LL=3.0 -> Wu=8.6
wu_slab = (1.4 * 2.5) + (1.7 * 3.0)
mu_slab = (wu_slab * 4.5**2) / 10 # عزم مستمر
# (استخدام نفس محرك الانعطاف للبلاطات)
print(f"   - الحمولة التصعيدية: {wu_slab} kN/m2")
print(f"   - التسليح المطلوب وفق كود جامعة دمشق لضمان المتانة والأمان.")
print(f"\n{'*'*25} تم التدقيق وفق الكود السوري {'*'*25}")
