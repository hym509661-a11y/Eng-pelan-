function calculateSlab(Ly, Lx, mainDiameter, liveLoad, finishingLoad) {
    // 1. تحديد نوع البلاطة واتجاه العمل
    const ratio = Ly / Lx;
    let type = (ratio > 2) ? "One-Way" : "Two-Way";

    // 2. حساب السماكة الدنيا (h) لتجنب السهم (بفرض مستمرة من طرف واحد)
    // h = L / 24 (حسب الكود السوري/الأمريكي للبلاطات باتجاه واحد)
    let h_min = (Lx * 100) / 24; 
    let h = Math.ceil(h_min); // تقريب لأقرب عدد صحيح

    // 3. حساب الحمولات (Kg/m2)
    const concreteDensity = 2500;
    const deadLoad = (h / 100) * concreteDensity + finishingLoad;
    const ultimateLoad = 1.2 * deadLoad + 1.6 * liveLoad;

    // 4. حساب العزوم (Moment) - لمنتصف المجاز (بسيط الاستناد كمثال)
    // M = (w * L^2) / 8
    const moment = (ultimateLoad * Math.pow(Lx, 2)) / 8;

    // 5. حساب مساحة الحديد (As) والعدد (بفرض d = h - 2cm)
    const d = h - 2.5; 
    const fy = 4000; // إجهاد الخضوع للحديد
    // معادلة تقريبية سريعة للمساحة
    let As = moment / (0.9 * fy * 0.9 * d); 
    
    // حساب الوزن المتر الطولي للقطر المختار
    const weightPerMeter = (Math.pow(mainDiameter, 2) / 162);
    const numberOfBars = Math.ceil(As / (0.785 * Math.pow(mainDiameter/10, 2)));

    return {
        slabType: type,
        thickness: h,
        totalDeadLoad: deadLoad.toFixed(2),
        requiredBars: (numberOfBars < 5) ? 5 : numberOfBars, // الحد الأدنى 5 قضبان
        concreteVolume: (Ly * Lx * (h / 100)).toFixed(2),
        totalSteelWeight: (numberOfBars * Lx * weightPerMeter * Ly).toFixed(2)
    };
}
