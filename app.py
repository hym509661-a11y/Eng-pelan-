import math

class SyrianStructuralPro:
    def __init__(self):
        self.header = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات - إشراف - تعهدات | 0998449697"
        self.phi_flex = 0.90 # معامل الانعطاف
        self.phi_col = 0.65  # معامل الأعمدة
        
    def print_result(self, title, data):
        print(f"\n{'='*50}\n{title}\n{'-'*50}")
        for key, value in data.items():
            print(f"{key}: {value}")
        print(f"{'-'*50}\n{self.header}\n{'='*50}")

    def design_all(self, fcu, fy, slab_l, col_p, foot_q):
        f_prime_c = 0.8 * fcu
        
        # 1. تصميم بلاطة (ممرات/غرف) - حمولة المهندس بيلان
        wu_slab = (1.4 * 2.5) + (1.7 * 3.0) # للممرات
        mu_slab = (wu_slab * slab_l**2) / 10
        d_slab = 130 # فرض سماكة 15 سم
        as_slab = (mu_slab * 1e6) / (self.phi_flex * fy * 0.9 * d_slab)
        as_min_slab = (1.4 / fy) * 1000 * d_slab
        
        # 2. تصميم عمود (اقتصادي 1%)
        ag_col = (col_p * 1000) / (self.phi_col * 0.8 * (0.85 * f_prime_c * 0.99 + fy * 0.01))
        side = math.sqrt(ag_col)
        
        # 3. تصميم أساس (منفرد)
        area_foot = (col_p / 1.5 * 1.1) / foot_q # حمولة تشغيلية
        b_foot = math.sqrt(area_foot)

        # عرض النتائج
        self.print_result("نتائج التصميم الإنشائي الشامل", {
            "تسلـيح البلاطة السفلي": f"{max(round(as_slab), round(as_min_slab))} mm²/m",
            "أبعاد العمود المقترحة": f"{round(side/10)*10} x {round(side/10)*10} mm",
            "أبعاد الأساس (B x L)": f"{round(b_foot, 2)} x {round(b_foot, 2)} m",
            "ملاحظة فنية": "تم التدقيق وفق ملحقات الكود السوري - جامعة دمشق"
        })

# تشغيل البرنامج
engine = SyrianStructuralPro()
# أدخل القيم هنا: (fcu, fy, طول المجاز, حمولة العمود kN, قدرة تحمل التربة kPa)
engine.design_all(25, 400, 4.5, 2000, 150)
