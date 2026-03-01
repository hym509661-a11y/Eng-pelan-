import math

# المدخلات (تأكد أن الأسماء تطابق المتغيرات في تطبيقك)
Ly = 27.0  # طول البلاطة
Lx = 2.0   # عرض البلاطة
main_dia = 12 # قطر الحديد بالـ mm

# 1. حساب السماكة h (تلقائياً)
# بفرض البلاطة مستمرة من طرف واحد (Lx/24)
h_cm = math.ceil((Lx * 100) / 24) 

# 2. حساب الأحمال (قيم افتراضية يمكنك ربطها بمدخلات)
dead_load = (h_cm / 100) * 2500 + 150  # وزن ذاتي + تغطية
live_load = 200 
wu = 1.2 * dead_load + 1.6 * live_load

# 3. حساب العزوم والتسليح
mu = (wu * (Lx**2)) / 8
d = h_cm - 2.5 # الارتفاع الفعال
# حساب مساحة الحديد المطلوبة (معادلة تقريبية سريعة)
as_req = mu / (0.9 * 4000 * 0.9 * d) 

# 4. حساب عدد القضبان ووزن الحديد
bar_area = (math.pi * (main_dia/10)**2) / 4
num_bars = math.ceil(as_req / bar_area)
if num_bars < 5: num_bars = 5 # الحد الأدنى للكود

weight_per_m = (main_dia**2) / 162
total_weight = num_bars * Lx * weight_per_m * Ly

# --- العرض على التطبيق ---
print(f"السماكة المقترحة: {h_cm} cm")
print(f"الحديد السفلي: {num_bars} T {main_dia} / m'")
print(f"إجمالي وزن الحديد: {total_weight:.2f} kg")
