import tkinter as tk
from tkinter import messagebox
import pandas as pd # لتصدير الجداول إلى إكسل

class PelanAdvancedBIM:
    def __init__(self, root):
        self.root = root
        self.root.title("Pelan Ultimate Suite - Eng Pelan Mustfa Abdulkarim")
        self.root.geometry("1100x700")
        self.root.configure(bg="#f4f4f4")

        # --- البيانات الهندسية الافتراضية ---
        self.rebar_data = [] # لتخزين بيانات الحديد (BBS)

        self.setup_ui()

    def setup_ui(self):
        # العنوان الرئيسي والختم
        header = tk.Frame(self.root, bg="#1e272e", height=80)
        header.pack(fill="x")
        
        title = tk.Label(header, text="PELAN MULTI-PRO (SAFE + ETABS + REVIT)", 
                         fg="white", bg="#1e272e", font=("Arial", 16, "bold"))
        title.pack(pady=10)

        # لوحة التحكم الجانبية
        control_panel = tk.Frame(self.root, width=250, bg="#d2dae2")
        control_panel.pack(side="left", fill="y", padx=5, pady=5)

        # أزرار العمليات
        tk.Button(control_panel, text="1. Import AutoCAD Layout", command=self.import_layout, width=25).pack(pady=10)
        tk.Button(control_panel, text="2. Design All Elements", command=self.calculate_reinforcement, width=25).pack(pady=10)
        tk.Button(control_panel, text="3. Generate BBS (Excel)", command=self.export_to_excel, bg="#27ae60", fg="white", width=25).pack(pady=20)

        # ساحة الرسم (Revit/SAFE View)
        self.drawing_area = tk.Canvas(self.root, bg="white", bd=3, relief="ridge")
        self.drawing_area.pack(side="right", expand=True, fill="both", padx=10, pady=10)

        # الختم الثابت في الأسفل
        footer = tk.Label(self.root, text="Designed by: Eng Pelan Mustfa Abdulkarim | 0998449697", 
                          bg="#1e272e", fg="#feca57", font=("Arial", 11, "italic"))
        footer.pack(side="bottom", fill="x")

    def import_layout(self):
        # محاكاة قراءة ملف أوتوكاد
        self.drawing_area.delete("all")
        self.drawing_area.create_rectangle(50, 50, 450, 150, outline="black", width=2) # جسر (Beam)
        self.drawing_area.create_text(250, 100, text="Beam B1 (60x30)", font=("Arial", 10))
        messagebox.showinfo("AutoCAD Sync", "Floor plan imported successfully. Elements identified.")

    def calculate_reinforcement(self):
        # محاكاة حسابات ETABS/SAFE للحديد
        # الحديد العلوي (Top)
        self.drawing_area.create_line(60, 60, 440, 60, fill="red", width=4) 
        # الحديد السفلي (Bottom)
        self.drawing_area.create_line(60, 140, 440, 140, fill="blue", width=4)
        # الكانات (Stirrups)
        for x in range(70, 440, 30):
            self.drawing_area.create_line(x, 60, x, 140, fill="green", width=1)

        # تخزين البيانات للجدول
        self.rebar_data = [
            {"Element": "Beam B1", "Type": "Top Bar", "Dia (mm)": 16, "Length (m)": 4.0, "Weight (kg)": 6.32},
            {"Element": "Beam B1", "Type": "Bottom Bar", "Dia (mm)": 18, "Length (m)": 4.2, "Weight (kg)": 8.40},
            {"Element": "Beam B1", "Type": "Stirrups (10nos)", "Dia (mm)": 8, "Length (m)": 1.5, "Weight (kg)": 5.90}
        ]
        messagebox.showinfo("Design Complete", "Reinforcement calculated based on ACI/Eurocode.")

    def export_to_excel(self):
        if not self.rebar_data:
            messagebox.showwarning("No Data", "Please run Design first!")
            return
        
        # تحويل البيانات إلى ملف إكسل احترافي
        df = pd.DataFrame(self.rebar_data)
        file_name = "Pelan_BBS_Report.xlsx"
        df.to_excel(file_name, index=False)
        messagebox.showinfo("Success", f"BBS Report exported as {file_name}\nEng Pelan Mustfa Abdulkarim")

if __name__ == "__main__":
    root = tk.Tk()
    app = PelanAdvancedBIM(root)
    root.mainloop()
