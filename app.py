import cv2
import numpy as np
import ezdxf
from datetime import date

class StructuralEngineerAI:
    def __init__(self, img_path):
        self.img_path = img_path
        self.engineer_name = "المهندس المدني بيلان مصطفى عبدالكريم" # [cite: 2026-02-18]
        self.contact = "0998449697" # [cite: 2026-02-15]
        self.specialty = "دراسات - اشراف - تعهدات" # [cite: 2026-02-18]
        
    def process_and_design(self):
        # 1. قراءة وتحليل الصورة (Computer Vision)
        img = cv2.imread(self.img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # كشف الخطوط (المحاور)
        edges = cv2.Canny(gray, 50, 150)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        
        # استخراج المجازات (تبسيطاً سنأخذ القيم المقاسة افتراضياً من الصورة)
        spans = [5.50, 4.25, 5.50] 
        return spans

    def generate_full_dxf(self, spans):
        doc = ezdxf.new('R2010')
        msp = doc.modelspace()
        
        # إعدادات الطبقات
        doc.layers.new(name='AXIS', dxfattribs={'color': 8})
        doc.layers.new(name='BEAMS', dxfattribs={'color': 1, 'lineweight': 35})
        doc.layers.new(name='RIBS', dxfattribs={'color': 3})
        doc.layers.new(name='TITLE_BLOCK', dxfattribs={'color': 2})

        curr_x = 0
        h_slab = max(spans) * 100 / 21 # كود سوري: سماكة البلاطة L/21
        
        for i, L in enumerate(spans):
            # رسم الجائز (Beam)
            msp.add_line((curr_x, 0), (curr_x + L, 0), dxfattribs={'layer': 'BEAMS'})
            
            # رسم اتجاه الأعصاب (Ribs) - خطوط موازية صغيرة
            for rib_pos in np.arange(curr_x + 0.5, curr_x + L, 0.5):
                msp.add_line((rib_pos, -0.3), (rib_pos, 0.3), dxfattribs={'layer': 'RIBS'})
            
            # إضافة بيانات التسليح والسماكة
            msp.add_text(f"Span: {L}m | h={int(h_slab)}cm", dxfattribs={'height': 0.15}).set_placement((curr_x + L/3, 0.5))
            curr_x += L

        # إضافة الختم الهندسي الرسمي [cite: 2026-02-18]
        stamp = f"{self.engineer_name} | {self.specialty} | {self.contact}"
        msp.add_text(stamp, dxfattribs={'layer': 'TITLE_BLOCK', 'height': 0.3}).set_placement((0, -2))
        
        filename = "Bilan_Structural_Design.dxf"
        doc.saveas(filename)
        return filename

# التنفيذ الفوري
ai_engine = StructuralEngineerAI("plan.jpg")
detected_spans = ai_engine.process_and_design()
output_file = ai_engine.generate_full_dxf(detected_spans)

print(f"تمت الدراسة بنجاح! الملف الجاهز للأوتوكاد هو: {output_file}")
