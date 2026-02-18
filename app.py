' ==========================================================
' برنامج التصميم الإنشائي المتكامل - الكود العربي السوري
' مصمم ليعمل كدوال مخصصة (User Defined Functions)
' ==========================================================

' 1. دالة حساب مساحة الحديد الرئيسي (سفلي أو علوي)
Function SyriaCode_As(Mu_kNm As Double, b_mm As Double, d_mm As Double, fck As MPa, fy As MPa) As Variant
    Dim Rn As Double, m As Double, rho As Double, As_req As Double
    Dim rho_min As Double, rho_max As Double
    
    ' تحويل العزم لنيوتن.ملم
    Dim Mu As Double: Mu = Mu_kNm * 10 ^ 6
    
    ' معاملات الكود السوري (Phi = 0.9 للإنعطاف)
    Rn = Mu / (0.9 * b_mm * d_mm ^ 2)
    m = fy / (0.85 * fck)
    
    ' حساب نسبة التسليح
    If (1 - (2 * m * Rn / fy)) < 0 Then
        SyriaCode_As = "المقطع صغير جداً"
        Exit Function
    End If
    
    rho = (1 / m) * (1 - Sqr(1 - (2 * m * Rn / fy)))
    
    ' الحدود الدنيا والعليا حسب الكود
    rho_min = 1.4 / fy
    ' قيمة تقريبية لـ Rho Max لضمان الانهيار المطيل
    rho_max = 0.5 * (0.85 * fck * 0.85 / fy) * (600 / (600 + fy))
    
    If rho < rho_min Then rho = rho_min
    
    If rho > rho_max Then
        SyriaCode_As = "تجاوز الحد الأعلى (Over Reinforced)"
    Else
        SyriaCode_As = Round(rho * b_mm * d_mm, 2) ' المساحة بـ ملم مربع
    End If
End Function

' 2. دالة حساب الكانات (تسليح القص)
Function SyriaCode_Stirrups(Vu_kN As Double, b As Double, d As Double, fck As Double, fyt As Double) As String
    Dim Vc As Double, Vs As Double, Av_s As Double
    ' مقاومة البيتون للقص (تبسيط الكود السوري)
    Vc = 0.9 * (1 / 6) * Sqr(fck) * b * d / 1000
    
    If Vu_kN <= 0.5 * Vc Then
        SyriaCode_Stirrups = "كانات إنشائية (T8@20cm)"
    Else
        Vs = (Vu_kN / 0.85) - Vc
        ' حساب Av/s
        Av_s = (Vs * 1000) / (fyt * d)
        SyriaCode_Stirrups = "مطلوب: " & Round(Av_s, 2) & " mm2/mm"
    End If
End Function

' 3. ماكرو إضافة الختم والبيانات الخاصة بك
Sub ApplyEngineeringStamp()
    Dim ws As Worksheet
    Set ws = ActiveSheet
    
    With ws.PageSetup
        .CenterFooter = "&""Arial,Bold""&12 التصميم تم وفق الكود العربي السوري - النسخة الأخيرة"
        .RightFooter = "&""Arial,Regular""&10 رقم الاعتماد: 0998449697"
        .LeftFooter = "&""Arial,Italic""&10 تاريخ الإصدار: " & Date
    End With
    
    MsgBox "تم تفعيل الختم المهني على تذييل الصفحة بنجاح.", vbInformation, "نظام التوثيق"
End Sub
