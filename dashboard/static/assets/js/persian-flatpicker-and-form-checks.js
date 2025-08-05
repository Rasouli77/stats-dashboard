flatpickr("#date-range", {
    inline: true,
    locale: "fa",
    mode: "range",
    dateFormat: "Y-m-d",
    onChange: function(selectedDates, dateStr, instance) {
    selectedRange = selectedDates;
    }
});
const filterProxyButton = document.getElementById("filter-proxy-button");
const realFilterForm = document.getElementById("filter-form");
filterProxyButton.addEventListener("click", () => {
    function formatJalaliDate(jdateObj) {
    if (!jdateObj || !jdateObj._cached_date) return "";
    const [year, month, day] = jdateObj._cached_date;
    return `${year}-${String(month).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
    }
    const fakeChecks = document.querySelectorAll(".fake-check");
    const realChecks = document.querySelectorAll(".real-check");
    let startDate = selectedRange[0]
    let endDate = selectedRange[1]
    let startJalaiDate = formatJalaliDate(startDate);
    let endJalaliDate = formatJalaliDate(endDate);
    const realJalaliStartDate = document.getElementById("start-date");
    const realJalaliEndDate = document.getElementById("end-date");
    realJalaliStartDate.value = startJalaiDate;
    realJalaliEndDate.value = endJalaliDate;
    fakeChecks.forEach((item) => {
    if (item.checked == true) {
        realChecks.forEach((sitem) => {
        if (item.value == sitem.value) {
            sitem.checked = true;
        }
        }); 
    } else {
        realChecks.forEach((sitem) => {
        if (item.value == sitem.value) {
            sitem.checked = false;
        }
        }); 
    }
    });
})