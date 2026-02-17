import streamlit as st
import ezdxf
import io

# إعدادات الصفحة
st.set_page_config(page_title="مهندس بلان - محرر الأوتوكاد", layout="centered")

def create_stamped_dxf(base_text):
    # 1. إنشاء ملف DXF جديد (إصدار متوافق R2010)
    doc = ezdxf.new('R2010')
    msp = doc.modelspace()

    # 2. إعداد نص الختم مع الرقم المطلوب في الذاكرة المحفوظة
    # النص سيظهر كالتالي: [نص المستخدم] | 0998449697
    final_stamp = f"{base_text} - 0998449697"

    # 3. إضافة الختم إلى الرسم (الإحداثيات 0,0)
    msp.add_text(
        final_stamp,
        dxfattribs={
            'height': 0.5,      # حجم الخط
            'color': 1,         # اللون الأحمر في أوتوكاد
            'style': 'Standard'
        }
    ).set_placement((10, 10))  # موقع الختم على المحاور

    # إضافة إطار بسيط حول الختم
    msp.add_lwpolyline([(5, 5), (50, 5), (50, 15), (5, 15), (5, 5)])

    # 4. حفظ الملف في ذاكرة مؤقتة (Buffer)
    out_buffer = io.StringIO()
    doc.write(out_buffer)
    return out_buffer.getvalue()

# --- واجهة المستخدم في Streamlit ---
st.title("🏗️ برنامج مهندس بلان")
st.subheader("توليد ملفات DXF مع الختم التلقائي")

st.info("سيتم إضافة الرقم 0998449697 تلقائياً في نهاية الختم.")

# مدخلات المستخدم
user_note = st.text_input("أدخل عنوان المخطط أو نص الختم:", "مخطط هندسي جديد")

if st.button("توليد وتحميل الملف"):
    try:
        dxf_content = create_stamped_dxf(user_note)
        
        # زر التحميل
        st.download_button(
            label="💾 تحميل ملف AutoCAD (DXF)",
            data=dxf_content,
            file_name="Engineer_Plan_Stamp.dxf",
            mime="application/dxf"
        )
        st.success("تم تجهيز الملف بنجاح مع الرقم المعتمد!")
    except Exception as e:
        st.error(f"حدث خطأ أثناء التوليد: {e}")

# تذييل الصفحة
st.markdown("---")
st.caption("برنامج مهندس بلان | الإصدار التجريبي 2026")
