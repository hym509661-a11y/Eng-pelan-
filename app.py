import tkinter as tk
from tkinter import messagebox

def calculate_column():
    try:
        # إدخال الحمولة التصميمية (Nu)
        nu = float(entry_load.get())
        # إدخال أبعاد العمود (b, h)
        b = float(entry_width.get())
        h = float(entry_height.get())
        
        # حساب مساحة البيتون Ac
        ac = b * h
        
        # حساب مساحة التسليح التقريبية (فرضية 1%)
        as_min = 0.01 * ac
        
        # نص الختم الخاص بك
        stamp_info = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات | 0998449697"
        
        result_text = f"--- نتائج التصميم ---\n"
        result_text += f"مساحة المقطع: {ac} cm²\n"
        result_text += f"التسليح المقترح: {as_min:.2f} cm²\n"
        result_text += f"\n--------------------\n{stamp_info}"
        
        label_result.config(text=result_text)
        
    except ValueError:
        messagebox.showerror("خطأ", "يرجى إدخال قيم عددية صحيحة")

# إنشاء الواجهة الرسومية (GUI)
root = tk.Tk()
root.title("برنامج الجواد المصغر - تصميم عناصر خرسانية")
root.geometry("400x500")

tk.Label(root, text="تصميم أعمدة خرسانية", font=("Arial", 14, "bold")).pack(pady=10)

# الحقول
tk.Label(root, text="الحمولة التصميمية Nu (kN):").pack()
entry_load = tk.Entry(root)
entry_load.pack()

tk.Label(root, text="عرض العمود b (cm):").pack()
entry_width = tk.Entry(root)
entry_width.pack()

tk.Label(root, text="ارتفاع العمود h (cm):").pack()
entry_height = tk.Entry(root)
entry_height.pack()

# زر الحساب
btn_calc = tk.Button(root, text="حساب وتسجيل الختم", command=calculate_column, bg="blue", fg="white")
btn_calc.pack(pady=20)

# منطقة النتائج
label_result = tk.Label(root, text="", justify="right")
label_result.pack(pady=10)

root.mainloop()
