import streamlit as st

# --- 1. بيانات المهندس بيلان (الختم الرسمي) ---
# تم تحديث الختم بناءً على طلبك بتاريخ 2026-02-18
engineer_name = "المهندس المدني بيلان مصطفى عبدالكريم"
engineer_info = "دراسات - اشراف - تعهدات"
engineer_phone = "0998449697"

# --- 2. مدخلات افتراضية (هنا نضع منطق الحسابات) ---
# لنفترض أننا نحسب عدد الأسياخ بناءً على القطر (مثلاً T16)
As_required = 3015.0  # المساحة الكلية
bar_diameter = 16
area_single_bar = (3.14159 * (bar_diameter**2)) / 4
num_bars = int(As_required / area_single_bar) + 1 # الناتج سيكون 15 سيخ تقريباً

# --- 3. منطق التلوين التلقائي (Dynamic Coloring) ---
# إذا زاد عدد الأسياخ عن 8 في الطبقة الواحدة نعتبره خطراً
bar_color = "#2e7d32" # أخضر (حالة آمنة)
warning_msg = ""

if num_bars > 8:
    bar_color = "#d32f2f" # أحمر (حالة مبالغ فيها)
    warning_msg = f"""
    <div style="background-color: #ffebee; color: #b71c1c; padding: 15px; border-radius: 8px; border-right: 5px solid #b71c1c; margin: 15px 0;">
        ⚠️ <b>تحذير هندسي:</b> عدد الأسياخ ({num_bars}) كبير جداً لمقطع واحد!<br>
        💡 <b>نصيحة بيلان:</b> جرب زيادة عمق الجائز أو استخدام قطر أكبر (T20) لتجنب التعشيش.
    </div>
    """

# --- 4. قالب التصميم النهائي (HTML + CSS) ---
design_html = f"""
<div style="direction: rtl; text-align: right; font-family: 'Tahoma', sans-serif; border: 2px solid #1e88e5; padding: 25px; border-radius: 15px; background-color: white; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
    
    <h2 style="color: #1e88e5; text-align: center; margin-bottom: 20px;">Petan Structural Analysis Pro</h2>
    
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px;">
        <p style="font-size: 18px; margin: 5px 0;">مساحة الحديد المطلوبة: <b>{As_required:.2f} mm²</b></p>
        <p style="font-size: 18px; margin: 5px 0;">التسليح المقترح: <span style="color: {bar_color}; font-weight: bold; font-size: 22px;">{num_bars} T {bar_diameter}</span></p>
    </div>

    {warning_msg}

    <div style="margin-top: 30px; padding: 15px; background-color: #e3f2fd; border-radius: 10px; border: 1px solid #1e88e5;">
        <h4 style="margin: 0; color: #0d47a1;">{engineer_name}</h4>
        <p style="margin: 5px 0; color: #455a64; font-size: 14px;">{engineer_info}</p>
        <p style="margin: 0; color: #1e88e5; font-weight: bold;">تواصل: {engineer_phone}</p>
    </div>
</div>
"""

# --- 5. العرض النهائي في Streamlit ---
st.markdown(design_html, unsafe_allow_html=True)
