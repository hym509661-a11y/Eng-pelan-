import tkinter as tk
from tkinter import messagebox

class SyrianEngineerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامج المهندس بيلان عبدالكريم - الكود السوري")
        self.root.geometry("450x600")
        
        # العنوان الرئيسي والختم
        tk.Label(root, text="المكتب الهندسي: بيلان مصطفى عبدالكريم", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(root, text="دراسات - إشراف - تعهدات | 0998449697", font=("Arial", 10)).pack()
        
        tk.Frame(height=2, bd=1, relief=tk.SUNKEN).pack(fill=tk.X, padx=10, pady=10)

        # مدخلات البيانات
        self.create_input("العزم التصميمي (Mu) طن.متر:", "12")
        self.create_input("عرض الجائز (b) سم:", "20")
        self.create_input("الارتفاع الفعال (d) سم:", "52")
        self.create_input("مقاومة البيتون (f'c) كغ/سم2:", "200")

        # زر الحساب
        self.calc_btn = tk.Button(root, text="احسب التسليح حسب الكود السوري", command=self.calculate, bg="#2c3e50", fg="white", font=("Arial", 10, "bold"))
        self.calc_btn.pack(pady=20)

        # منطقة النتائج
        self.result_label = tk.Label(root, text="النتائج ستظهر هنا", font=("Arial", 11, "italic"), fg="blue", justify="right")
        self.result_label.pack(pady=10)

    def create_input(self, label_text, default_val):
        frame = tk.Frame(self.root)
        frame.pack(fill=tk.X, padx=20, pady=5)
        lbl = tk.Label(frame, text=label_text, width=25, anchor="e")
        lbl.pack(side=tk.RIGHT)
        ent = tk.Entry(frame)
        ent.insert(0, default_val)
        ent.pack(side=tk.RIGHT, expand=True, padx=5)
        setattr(self, label_text.split('(')[0].strip(), ent)

    def calculate(self):
        try:
            # جلب البيانات من الواجهة
            Mu = float(getattr(self, "العزم التصميمي").get()) * 10**5
            b = float(getattr(self, "عرض الجائز").get())
            d = float(getattr(self, "الارتفاع الفعال").get())
            fpc = float(getattr(self, "مقاومة البيتون").get())
            fy = 3600
            
            # المعادلات البرمجية (الكود السوري)
            rn = Mu / (0.9 * b * d**2)
            import math
            rho = (0.85 * fpc / fy) * (1 - math.sqrt(1 - (2.353 * rn / fpc)))
            rho_min = max(14/fy, (0.25 * math.sqrt(fpc))/fy)
            rho = max(rho, rho_min)
            as_req = rho * b * d
            
            # عرض النتيجة بختم المهندس
            res_text = f"مساحة الحديد المطلوبة: {as_req:.2f} cm2\n"
            res_text += f"التسليح المقترح: {math.ceil(as_req/2.01)} T 16\n"
            res_text += "\nتمت الدراسة: م. بيلان عبدالكريم"
            
            self.result_label.config(text=res_text, fg="green")
        except Exception as e:
            messagebox.showerror("خطأ", "يرجى التأكد من إدخال أرقام صحيحة")

if __name__ == "__main__":
    root = tk.Tk()
    app = SyrianEngineerApp(root)
    root.mainloop()
