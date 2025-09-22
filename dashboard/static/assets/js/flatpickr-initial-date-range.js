// Initialize
const inFlatPicker = document.querySelector("#date-range")._flatpickr;
// Returns all 2 dates: the start and the end of the last 7 days
const {inStartDate, inEndDate} = getJalaliDateRange();
// Update it on page load accordingly
// This triggers on page load
document.addEventListener("DOMContentLoaded", () => {
    inFlatPicker.setDate([inStartDate, inEndDate], true);
});