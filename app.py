// --- كود برنامج Petan Structural Analysis Pro ---

const engineerData = {
    name: "المهندس المدني بيلان مصطفى عبدالكريم",
    info: "دراسات - اشراف - تعهدات",
    phone: "0998449697"
};

function calculateDesign(width, depth, Mu, fc, fy) {
    try {
        let d = depth - 50; // العمق الفعال
        let As = Mu / (0.9 * fy * 0.85 * d); // حساب تقريبي للمساحة
        
        // التحقق من نسبة التسليح القصوى
        let rho = As / (width * d);
        let rhoMax = 0.02; // قيمة افتراضية للتبسيط
        
        let warnings = [];
        if (rho > rhoMax) {
            warnings.push("⚠️ المقطع متجاوز للنسبة القصوى (Over-Reinforced)");
            warnings.push("💡 نصيحة بيلان: يرجى زيادة عمق المقطع لتوفير الحديد");
        }

        // عرض النتائج في الصفحة
        renderResults(As, warnings);
        
    } catch (error) {
        console.error("حدث خطأ في الحسابات:", error);
    }
}

function renderResults(As, warnings) {
    // هذا الجزء هو المسؤول عن ملء الصفحة البيضاء
    const displayArea = document.getElementById('results'); 
    if(displayArea) {
        displayArea.innerHTML = `
            <h3>مساحة الحديد المطلوبة: ${As.toFixed(2)} mm²</h3>
            <div style="color: red;">${warnings.join('<br>')}</div>
            <hr>
            <p><b>${engineerData.name}</b></p>
            <p>${engineerData.info}</p>
            <p>${engineerData.phone}</p>
        `;
    }
}
