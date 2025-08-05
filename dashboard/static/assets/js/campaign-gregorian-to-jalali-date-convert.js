function convertGregorianToJalali(gregorianDateStr) {
    const [gy, gm, gd] = gregorianDateStr.split("-").map(Number);
    const { jy, jm, jd } = jalaali.toJalaali(gy, gm, gd);
    return `${jy}/${String(jm).padStart(2, '0')}/${String(jd).padStart(2, '0')}`;
}
const dates = document.querySelectorAll(".date");
document.addEventListener("DOMContentLoaded", () => {
    dates.forEach((date) => {
        date.innerHTML = convertGregorianToJalali(date.innerHTML);
    });
})