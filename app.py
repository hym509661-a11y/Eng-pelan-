def generate_report(element_name, dimensions, loads, reinforcement):
    report = f"""
    --------------------------------------------------
    المهندس المدني: بيلان مصطفى عبدالكريم
    دراسات - إشراف - تعهدات
    هاتف: 0998449697
    --------------------------------------------------
    تقرير دراسة العنصر: {element_name}
    الأبعاد: {dimensions}
    الحمولات المطبقة: {loads}
    التسليح المعتمد: {reinforcement}
    --------------------------------------------------
    تمت الدراسة وفق الكود العربي السوري لعام 2012
    """
    with open(f"{element_name}_report.txt", "w", encoding="utf-8") as file:
        file.write(report)
    print("تم توليد التقرير بنجاح.")

# مثال تشغيل
generate_report("G1", "20x60", "3.5 t/m", "4 T 12")
