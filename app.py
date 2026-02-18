import streamlit as st

# --- 1. الختم الرسمي للمهندس بيلان ---
# تم تحديث النص وفقاً لطلبك بتاريخ 2026-02-18
st_name = "المهندس المدني بيلان مصطفى عبدالكريم"
st_info = "دراسات - اشراف - تعهدات"
st_phone = "0998449697" # [cite: 2026-02-15]

# --- 2. محاكاة النتائج (تأكد أن هذه المتغيرات موجودة في حساباتك) ---
As_val = 3015.93  
num_bars = 15
bar_phi = 16

# --- 3. تحديد اللون بناءً على المنطق الهندسي ---
# إذا كان عدد الأسياخ مبالغاً فيه (أكثر من 8) يظهر باللون الأحمر
if num_bars > 8:
    text_color = "#d32f2f" # أحمر
    warning_box = f'<div style="background-color: #ffebee; color: #b71c1c; padding: 10px; border-radius: 5px; border-right: 5px solid #b71c1c; margin-bottom: 15px;">⚠️ تحذير: عدد الأسياخ ({num_bars}) كبير جداً. يرجى مراجعة العمق الإنشائي.</div>'
else:
    text_color = "#2e7d32" # أخضر
    warning_box = ""

# --- 4. العرض النهائي (استخدام علامة الثلاث تنصيص لتجنب أخطاء السطور) ---
design_template = f"""
<div style="direction: rtl; text-align: right; font-family: sans-serif; border: 2px solid #1E88E5; padding: 20px; border-radius: 10px; background-color: white;">
    <h3 style="color: #1E88E5; margin-top: 0;">نتائج تصميم برنامج Petan</h3>
    
    <p style="font-size: 18px;">مساحة الحديد: <b>{As_val:.2f} mm²</b></p>
    
    <p style="font-size: 20px;">التسليح العلوي: <span style="color: {text_color}; font-weight: bold;">{num_bars} T {bar_phi}</span></p>
    
    {warning_box}
    
    <div style="margin-top: 20px; padding-top: 10px; border-top: 1px solid #eee;">
        <p style="margin: 0; font-weight: bold; color: #333;">{st_name}</p>
        <p style="margin: 3px 0; color: #666; font-size: 14px;">{st_info}</p>
        <p style="margin: 0; color: #1E88E5;">هاتف: {st_phone}</p>
    </div>
</div>
"""

# عرض الكود في واجهة Streamlit
st.markdown(design_template, unsafe_allow_html=True)
