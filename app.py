# ==========================================
# مبرمج بواسطة: المهندس بيلان مصطفى عبدالكريم
# اختصاص: دراسات - اشراف - تعهدات
# موبايل: 0998449697
# ==========================================

def calculate_beam_data(B_cm, H_cm, L_m, DL_kn, LL_kn):
    # 1. حساب الحمل التصميمي (Ultimate Load)
    # المعادلة: Wu = 1.2*DL + 1.6*LL
    wu = (1.2 * DL_kn) + (1.6 * LL_kn)

    # 2. حساب العزم التصميمي (kN.m) لجوائز بسيطة الاستناد
    mu = (wu * (L_m**2)) / 8

    # 3. بيانات التسليح (كما في تطبيقك)
    main_steel = "4 T 16"
    top_steel = "2 T 12"
    stirrups = "T 8 @ 15cm"

    # 4. مخرجات البرنامج مع الختم المهني
    return {
        "ultimate_load": f"{wu:.2f} kN/m",
        "max_moment": f"{mu:.2f} kN.m",
        "reinforcement": {
            "main": main_steel,
            "top": top_steel,
            "links": stirrups
        },
        "engineer_stamp": "المهندس المدني بيلان مصطفى عبدالكريم | 0998449697"
    }

# مثال لتجربة الكود (بناءً على أرقام صورك):
# B=30, H=60, L=5.00, DL=25.00, LL=15.00
result = calculate_beam_data(30, 60, 5.0, 25.0, 15.0)

print(f"الحمل التصميمي: {result['ultimate_load']}")
print(f"التوقيع المهني: {result['engineer_stamp']}")
