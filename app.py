import streamlit as st

# --- 1. البيانات الشخصية المحدثة ---
# [cite: 2026-02-18]
engineer_name_en = "Eng. Pelan Mustafa Abdulkarim"
engineer_name_ar = "المهندس المدني بيلان مصطفى عبدالكريم"
engineer_info = "دراسات - اشراف - تعهدات"
engineer_phone = "0998449697" # [cite: 2026-02-15]

# --- 2. متغيرات الحسابات (تأكد أنها مطابقة لمتغيراتك) ---
As_val = 3015.93  
num_bars = 15     
bar_phi = 16

# --- 3. منطق التلوين والتحذير ---
# إذا زاد العدد عن 8 يظهر باللون الأحمر
res_color = "#d32f2f" if num_bars > 8 else "#2e7d32"
warning_text = ""
if num_bars > 8:
    warning_text = f"""
    <div style="background-color: #ffebee; color: #b71c1c; padding: 10px; border-radius: 5px; margin: 10px 0; border-right: 5px solid #b71c1c;">
        ⚠️ تحذير هندسي: العدد ({num_bars}) مبالغ فيه لمقطع واحد. يفضل زيادة العمق.
    </div>
    """

# --- 4. بناء قالب التصميم (HTML) ---
design_template = f"""
<div style="direction: rtl; text-align: right; font-family: sans-serif; border: 2px solid #1e88e5; padding: 20px; border-radius: 15px; background-color: #ffffff;">
    <h2 style="color: #1e88e5; text-align: center; margin-bottom: 20px;">Petan Structural Pro</h2>
    
    <p style="font-size: 18px; margin: 5px 0;">مساحة الحديد المطلوبة: <b>{As_val:.2f} mm²</b></p>
    <p style="font-size: 20px; margin: 10px 0;">التسليح: <span style="color: {res_color}; font-weight: bold;">{num_bars} T {bar_phi}</span></p>
    
    {warning_text}
    
    <div style="margin-top: 30px; padding: 15px; background-color: #f1f8e9; border-radius: 10px; border: 1px dashed #2e7d32;">
        <h4 style="margin: 0; color: #1b5e20;">{engineer_name_ar}</h4>
        <p style="margin: 5px 0; color: #455a64;">{engineer_info}</p>
        <p style="margin: 0; color: #1e88e5; font-weight: bold;">تواصل: {engineer_phone}</p>
    </div>
</div>
"""

# --- 5. الخطوة الذهبية التي ستحل المشكلة ---
# تأكد من استخدام st.markdown مع unsafe_allow_html=True
st.markdown(design_template, unsafe_allow_html=True)
