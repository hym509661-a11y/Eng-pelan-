import streamlit as st

# 1. تعريف البيانات الشخصية (الختم)
engineer_name = "المهندس المدني بيلان مصطفى عبدالكريم"
engineer_info = "دراسات - اشراف - تعهدات"
engineer_phone = "0998449697"

# 2. منطق الحسابات (مثال)
# افترضنا أن هذه المتغيرات قادمة من المدخلات في برنامجك
As_required = 3015.93  # مساحة افتراضية (مثلاً 15 T 16)
is_over_reinforced = True # حالة افتراضية للتجربة

# 3. صياغة التنبيهات
warnings_html = ""
if is_over_reinforced:
    warnings_html = """
    <div style="color: #D32F2F; background-color: #FFEBEE; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
        ⚠️ <b>تنبيه هندسي:</b> المقطع متجاوز للنسبة القصوى. <br>
        💡 نصيحة بيلان: يرجى زيادة عمق المقطع لتوفير الحديد وضمان سلامة الصب.
    </div>
    """

# 4. تجميع مخرجات التصميم والختم في قالب واحد
design_output = f"""
<div style="direction: rtl; text-align: right; font-family: sans-serif; border: 2px solid #1E88E5; padding: 20px; border-radius: 15px;">
    <h2 style="color: #1E88E5; border-bottom: 1px solid #ddd; padding-bottom: 10px;">نتائج التصميم الإنشائي</h2>
    
    <p style="font-size: 18px;">مساحة الحديد المطلوبة: <span style="color: #2E7D32; font-weight: bold;">{As_required:.2f} mm²</span></p>
    
    {warnings_html}
    
    <div style="margin-top: 30px; padding-top: 15px; border-top: 2px dashed #1E88E5; background-color: #f9f9f9; padding: 10px; border-radius: 10px;">
        <h4 style="margin: 0; color: #333;">{engineer_name}</h4>
        <p style="margin: 5px 0; color: #666;">{engineer_info}</p>
        <p style="margin: 0; color: #1E88E5; font-weight: bold;">هاتف: {engineer_phone}</p>
    </div>
</div>
"""

# 5. عرض النتيجة النهائية في واجهة Streamlit
st.markdown(design_output, unsafe_allow_html=True)
