import tkinter as tk
from tkinter import messagebox
import math

class SyrianDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج التصميم الإنشائي - م. بيلان مصطفى")
        self.root.geometry("500x650")
        
        # الختم المهني المحفوظ
        self.stamp_text = "المهندس المدني بيلان مصطفى عبدالكريم\nدراسات-اشراف-تعهدات 0998449697"

        # واجهة المدخلات
        tk.Label(root, text="نظام التصميم الإنشائي (الكود السوري)", font=("Arial", 14, "bold")).pack(pady=10)
        
        # مدخلات البلاطة
        tk.Label(root, text="طول مجاز البلاطة (متر):").pack()
        self.ent_l = tk.Entry(root); self.ent_l.pack(); self.ent_l.insert(0, "4.5")

        # مدخلات العمود
        tk.Label(root, text="حمولة العمود التصعيدية Pu (kN):").pack()
        self.ent_pu = tk.Entry(root); self.ent_pu.pack(); self.ent_pu.insert(0, "2000")

        # مدخلات الأساس
        tk.Label(root, text="قدرة تحمل التربة q_allow (kPa):").pack()
        self.ent_q = tk.Entry(root); self.ent_q.pack(); self.ent_q.insert(0, "150")

        # زر الحساب
        tk.Button(root, text="احسب النتائج بختم المهندس", command=self.calculate, bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=20)

        # منطقة النتائج
        self.text_result = tk.Text(root, height=15, width=50)
        self.text_result.pack(pady=10)

    def calculate(self):
        try:
            L = float(self.ent_l.get())
            Pu = float(self.ent_pu.get())
            q_allow = float(self.ent_q.get())
            fcu = 25
            fy = 400
            f_prime_c = 0.8 * fcu # تحويل للمقاومة الأسطوانية حسب الكود السوري

            # 1. حساب البلاطة (الممرات: 2.5 ميتة، 3 حية)
            wu = (1.4 * 2.5) + (1.7 * 3) # Wu = 8.6
            mu = (wu * L**2) / 10 # عزم مستمر
            d = 130 # لبلاطة 15سم
            as_req = (mu * 1e6) / (0.9 * fy * 0.9 * d)
            as_min = (1.4 / fy) * 1000 * d
            final_as = max(as_req, as_min) # حل مشكلة عدم ظهور التسليح السفلي

            # 2. حساب العمود (اقتصادي 1%)
            ag_col = (Pu * 1000) / (0.65 * 0.8 * (0.85 * f_prime_c * 0.99 + fy * 0.01))
            side = math.sqrt(ag_col)

            # 3. حساب الأساس (مربع)
            area_f = (Pu / 1.55 * 1.1) / q_allow
            b_f = math.sqrt(area_f)

            # عرض النتائج
            self.text_result.delete(1.0, tk.END)
            res = f"نتائج التصميم الإنشائي:\n"
            res += f"{'-'*40}\n"
            res += f"🏗️ تسليح البلاطة السفلي: {round(final_as)} mm2/m\n"
            res += f"🏛️ مقطع العمود الاقتصادي: {round(side/10)*10} x {round(side/10)*10} mm\n"
            res += f"🧱 أبعاد الأساس (B x L): {round(b_f, 2)} x {round(b_f, 2)} m\n"
            res += f"{'-'*40}\n"
            res += f"{self.stamp_text}"
            
            self.text_result.insert(tk.END, res)
            
        except Exception as e:
            messagebox.showerror("خطأ", "يرجى التأكد من إدخال أرقام صحيحة")

if __name__ == "__main__":
    root = tk.Tk()
    app = SyrianDesignApp(root)
    root.mainloop()
