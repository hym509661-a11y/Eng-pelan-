import math

class PetanStructuralPro:
    def __init__(self):
        self.engineer_name = "المهندس المدني بيلان مصطفى عبدالكريم"
        self.specialty = "دراسات - اشراف - تعهدات"
        self.phone = "0998449697"

    def analyze_beam(self, width, depth, Mu, fc, fy, cover=40):
        d = depth - cover - 10  # العمق الفعال التقريبي
        
        # 1. حساب مساحة الحديد المطلوبة (As)
        # Rn = Mu / (phi * b * d^2) ... 
        phi = 0.9
        if d <= 0: return "خطأ في الأبعاد"
        
        # معادلة تقريبية للتوضيح
        As_req = Mu / (0.9 * fy * 0.9 * d) 
        
        # 2. التحقق من نسبة التسليح القصوى (Rho Max)
        rho_actual = As_req / (width * d)
        beta1 = 0.85 if fc <= 28 else max(0.65, 0.85 - 0.05 * (fc - 28) / 7)
        rho_max = 0.85 * beta1 * (fc / fy) * (0.003 / (0.003 + 0.004))
        
        results = []
        
        # 3. نظام التنبيهات الذكي
        if rho_actual > rho_max:
            results.append("⚠️ خطأ: المقطع متجاوز للنسبة القصوى (Over-Reinforced).")
            results.append(f"💡 نصيحة بيلان: يرجى زيادة عمق المقطع عن {depth} مم.")
        
        # 4. خوارزمية التوفير (Optimization)
        new_depth = depth + 100
        As_saved = Mu / (0.9 * fy * 0.9 * (new_depth - cover - 10))
        saving = ((As_req - As_saved) / As_req) * 100
        if saving > 15:
            results.append(f"💰 خيار اقتصادي: زيادة العمق 10سم توفر {int(saving)}% من الحديد.")

        return {
            "As_required": round(As_req, 2),
            "Warnings": results,
            "Stamp": f"{self.engineer_name}\n{self.specialty}\n{self.phone}"
        }

# --- مثال على التنفيذ ---
petan_app = PetanStructuralPro()
# إدخال بيانات (عرض 250، عمق 400، عزم كبير)
design = petan_app.analyze_beam(250, 400, 150000000, 25, 400)

print("--- مخرجات برنامج Petan Structural Analysis Pro ---")
print(f"مساحة الحديد المطلوبة: {design['As_required']} mm²")
for note in design['Warnings']:
    print(note)
print("-" * 30)
print(design['Stamp'])
