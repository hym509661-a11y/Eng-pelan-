import tkinter as tk
from tkinter import filedialog, messagebox
import ezdxf # مكتبة لقراءة ملفات الأوتوكاد

class PelanEngineeringSuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Pelan Engineering Suite - Eng Pelan Mustfa Abdulkarim")
        self.root.geometry("900x600")
        
        # --- القائمة العلوية ---
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # إضافة أقسام البرامج المتكاملة
        self.add_modules()

        # --- واجهة العرض الرئيسية ---
        self.canvas = tk.Canvas(root, bg="white", width=700, height=500)
        self.canvas.pack(pady=20, expand=True)

        # --- منطقة الختم الشخصي (Stamp) ---
        self.footer = tk.Label(
            root, 
            text="Eng Pelan Mustfa Abdulkarim | Tel: 0998449697",
            font=("Arial", 10, "bold"),
            fg="navy"
        )
        self.footer.pack(side="bottom", fill="x")

        self.status_label = tk.Label(root, text="Ready to import AutoCAD floor plan...", bd=1, relief="sunken", anchor="w")
        self.status_label.pack(side="bottom", fill="x")

    def add_modules(self):
        # قسم الأوتوكاد و ETABS و SAFE
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Modules", menu=file_menu)
        file_menu.add_command(label="Import AutoCAD (DWG/DXF)", command=self.import_dxf)
        file_menu.add_separator()
        file_menu.add_command(label="ETABS Analysis", command=lambda: self.switch_mode("ETABS"))
        file_menu.add_command(label="SAFE Foundation", command=lambda: self.switch_mode("SAFE"))
        file_menu.add_command(label="Revit 3D Modeling", command=lambda: self.switch_mode("Revit"))

    def import_dxf(self):
        file_path = filedialog.askopenfilename(filetypes=[("AutoCAD Files", "*.dxf")])
        if file_path:
            try:
                doc = ezdxf.readfile(file_path)
                msp = doc.modelspace()
                self.status_label.config(text=f"Loaded: {file_path}")
                self.render_dwg_preview(msp)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def render_dwg_preview(self, msp):
        # محاكاة لعرض المسقط المعماري للبدء بتوزيع العناصر (بلاطات، أعمدة)
        self.canvas.delete("all")
        self.canvas.create_text(350, 250, text="[Floor Plan Preview Area]\nSelect elements to define as Columns/Beams", fill="gray")
        messagebox.showinfo("SAFE Mode", "You can now define structural elements (Slabs, Columns) on the layout.")

    def switch_mode(self, mode):
        self.status_label.config(text=f"Switched to {mode} Environment...")

# تشغيل البرنامج
if __name__ == "__main__":
    root = tk.Tk()
    app = PelanEngineeringSuite(root)
    root.mainloop()
