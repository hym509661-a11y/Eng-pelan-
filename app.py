class SyrianCodeDesign:
    def __init__(self, fcu, fy, gamma_c=1.5, gamma_s=1.15):
        self.fcu = fcu  # المقاومة المميزة للخرسانة
        self.fy = fy    # إجهاد الخضوع للحديد
        self.gamma_c = gamma_c # عامل أمان الخرسانة
        self.gamma_s = gamma_s # عامل أمان الحديد

    def get_fc_design(self):
        # المقاومة التصميمية حسب الكود السوري
        return 0.85 * self.fcu / self.gamma_c

    def check_min_steel(self, element_type, area):
        # تطبيق نسب التسليح الدنيا لكل عنصر (أعمدة 0.008, جوائز 0.0025...)
        limits = {"column": 0.008, "beam": 0.0025, "slab": 0.0018}
        return area * limits.get(element_type, 0.002)

# تذييل البرنامج بالرقم المطلوب آلياً في التقارير
def generate_report(results):
    report = f"المذكرة الحسابية - الكود السوري\n{results}\n"
    report += "-----------------------------------\n"
    report += "تم التصميم برمجياً وفق ملحقات الكود السوري لعام 2023\n"
    report += "للتواصل والاستفسار الفني: 0998449697"
    return report
