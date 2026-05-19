import ezdxf

def create_ribbed_slab(filename, rooms):
    # إنشاء ملف DXF جديد (متوافق مع أوتوكاد 2010 فما فوق)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # تعريف الطبقات (Layers) بألوان مهنية
    doc.layers.new(name='COLUMNS', dxfattribs={'color': 1}) # أحمر
    doc.layers.new(name='BEAMS', dxfattribs={'color': 5})   # أزرق
    doc.layers.new(name='RIBS', dxfattribs={'color': 8})    # رمادي
    doc.layers.new(name='TEXT', dxfattribs={'color': 7})    # أبيض

    for room in rooms:
        name = room['name']
        x, y = room['pos']
        w, h = room['dim']
        
        # 1. رسم حدود الغرفة (الجوائز المحيطة)
        msp.add_lwpolyline([(x, y), (x+w, y), (x+w, y+h), (x, y+h), (x, y)], 
                           dxfattribs={'layer': 'BEAMS', 'lineweight': 30})

        # 2. العمليات الحسابية لتوزيع الأعصاب (Engineering Logic)
        # نختار الاتجاه القصير دوماً لتوفير الحديد وتقليل الترخيم
        spacing = 0.50  # المسافة بين محاور الأعصاب (40 سم بلوك + 10 سم عصب)
        
        if w <= h: # الاتجاه القصير هو X (الأعصاب أفقية)
            num_ribs = int(h / spacing)
            for i in range(1, num_ribs):
                y_rib = y + (i * spacing)
                msp.add_line((x, y_rib), (x + w, y_rib), dxfattribs={'layer': 'RIBS'})
        else: # الاتجاه القصير هو Y (الأعصاب رأسية)
            num_ribs = int(w / spacing)
            for i in range(1, num_ribs):
                x_rib = x + (i * spacing)
                msp.add_line((x_rib, y), (x_rib, y + h), dxfattribs={'layer': 'RIBS'})

        # 3. إضافة نصوص توضيحية
        msp.add_text(f"{name} ({w}x{h})", 
                     dxfattribs={'layer': 'TEXT', 'height': 0.2}).set_pos((x+0.2, y+h-0.3))

    # حفظ الملف
    doc.saveas(filename)
    print(f"تم توليد المخطط بنجاح: {filename}")

# --- إدخالات مشروعك (150 متر مربع) بناءً على المعماري ---
# الإحداثيات (pos) والأبعاد (dim) مأخوذة من المخطط الذي أرسلته
my_project_rooms = [
    {'name': 'Salon', 'pos': (0, 0), 'dim': (3.5, 5.5)},
    {'name': 'Bedroom 1', 'pos': (3.5, 0), 'dim': (3.5, 5.5)},
    {'name': 'Kitchen', 'pos': (0, 5.5), 'dim': (3.1, 4.5)},
    {'name': 'Stairs', 'pos': (3.1, 5.5), 'dim': (2.4, 3.0)},
    {'name': 'Room 3', 'pos': (5.5, 5.5), 'dim': (3.3, 5.0)},
]

create_ribbed_slab("Pelan_Structural_Plan.dxf", my_project_rooms)
