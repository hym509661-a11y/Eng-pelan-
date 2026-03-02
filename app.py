import math

class SyrianStructuralPro:
    def __init__(self):
        # الختم المهني الخاص بك
        self.stamp = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات 0998449697"
        self.fcu = 25  # المقاومة المكعبة
        self.fy = 400  # إجهاد الخضوع للحديد

    def design_all(self, L_slab, P_col, q_soil):
        print("="*50)
        print(self.stamp)
        print("="*50)

        # 1. تصميم البلاطة (الممرات) - وفق أحمالك (2.5 ميتة، 3 حية)
        wu = (1.4 * 2.5) + (1.7 * 3.0) # Wu = 8.6 kN/m2
        Mu = (wu * L_slab**2) / 10     # عزم تصميمي
        d = 130 # سماكة فعالة لبلاطة 15 سم
        
        # حساب التسليح السفلي (جامعة دمشق)
        as_req = (Mu * 1e6) / (0.9 * self.fy * 0.9 * d)
        as_min = (1.4 / self.fy) * 1000 * d
        final_as = max(as_req, as_min)
        
        # 2. تصميم العمود (اقتصادي 1%)
        f_prime_c = 0.8 * self.fcu
        Ag = (P_col * 1000) / (0.65 * 0.8 * (0.85 * f_prime_c * 0.99 + self.fy * 0.01))
        side = math.sqrt(Ag)

        # 3. تصميم الأساس (منفرد)
        area_f = (P_col / 1.55 * 1.1) / q_soil # حمولة تشغيلية + وزن ذاتي
        b_f = math.sqrt(area_f)

        # عرض النتائج النهائية
        print(f"📍 نتائج تصميم البلاطة: {round(final_as)} مم2/م")
        print(f"📍 أبعاد العمود المقترحة: {round(side/10)*10} مم")
        print(f"📍 أبعاد الأساس: {round(b_f, 2)} م")
        print("-" * 50)
        print("تم التصميم وفق ملحقات الكود السوري بدقة واقتصاد")

# تشغيل فوري للتجربة
app = SyrianStructuralPro()
# (طول المجاز 4م، حمل العمود 1500kN، تحمل التربة 150)
app.design_all(4.0, 1500, 150)
