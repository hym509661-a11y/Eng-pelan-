import streamlit as st

# 1. البيانات الشخصية (الختم المعتمد)
# [cite: 2026-02-18]
name = "المهندس المدني بيلان مصطفى عبدالكريم"
job = "دراسات - اشراف - تعهدات"
phone = "0998449697" # [cite: 2026-02-15]

# 2. حسابات افتراضية (تأكد من وجودها في كودك)
As_val = 3015.93
num_bars = 15
bar_phi = 16

# 3. تحديد حالة التصميم واللون
# إذا كان عدد الأسياخ > 8 نعتبره مبالغاً فيه (أحمر)
color = "#d32f2f" if num_bars > 8 else "#2e7d32"

# 4. بناء القالب (هنا السر في التنسيق)
# لاحظ استخدام f-string مع st.markdown
design_html = f"""
<div style="direction: rtl; text-align: right; border: 2px solid #1E88E5; padding: 15px; border-radius: 10px; background-color: #ffffff;">
    <h3 style="color: #1E88E5; margin-bottom: 10px;">نتائج تصميم برنامج Petan</h3>
    
    <p style="font-size: 16px; margin: 5px 0;">مساحة الحديد: <b>{As_val:.2f} mm²</b></p>
    
    <p style="font-size: 18px; margin: 5px 0;">التسليح: <span style="color: {color}; font-weight: bold;">{num_bars} T {bar_phi}</span></p>
    
    <div style="background-color: #ffebee; color: #b71c1c; padding: 10px; border-radius: 5px; margin: 10px 0; font-weight: bold;">
        ⚠️ تنبيه: العدد مبالغ فيه! يرجى زيادة العمق لتوفير الحديد.
    </div>
    
    <hr style="border: 0.5px solid #eee;">
    
    <div style="font-size: 14px;">
        <p style="margin: 0; font-weight: bold;">{name}</p>
        <p style="margin: 2px 0;">{job}</p>
        <p style="margin: 0; color: #1E88E5;">هاتف: {phone}</p>
    </div>
</div>
"""

# 5. السطر الأهم الذي سيحل مشكلة ظهور الأكواد
st.markdown(design_html, unsafe_allow_html=True)
