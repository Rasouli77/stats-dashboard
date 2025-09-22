// Initialize
const currentURL = window.location.href;
const parsedURL = new URL(currentURL);
const urlType = parsedURL.searchParams.get("type");
//Titles
const titleOne = document.getElementById("title-type-1");
const titleTwo = document.getElementById("title-type-2");
const titleThree = document.getElementById("title-type-3");
// Display Toggle
const displayToggle = document.getElementById("chart-display-toggle");
// TCR
const aggConPercentChart = document.getElementById("ratio-container");
// BTCR
const branchConPercentChart = document.getElementById("ratio-container-multi-branch");
// EV
const aggEntryValChart = document.getElementById("second-ratio-container");
// BEV
const branchEntryValChart = document.getElementById("second-ratio-container-multi-branch");
// BTS
const oneToAllEntryChart =  document.getElementById("one-to-all-container");
// TBTS
const allToAllEntryChart = document.getElementById("second-one-to-all-container");
// Title Display Function
function showTitleAnalysis(one, two, three) {
    // one is always dispalyed
    one.style.display = "block";
    // The rest are hidden
    two.style.display = "none";
    three.style.display = "none";
}
// Chart Display Function
function showChartAnalysis(one, two, three, four, five, six) {
    // one is always dispalyed
    one.style.display = "block";
    // The rest are hidden
    two.style.display = "none";
    three.style.display = "none";
    four.style.display = "none";
    five.style.display = "none";
    six.style.display = "none";
}
if (urlType === '1') {
    showTitleAnalysis(titleOne, titleTwo, titleThree);
    showChartAnalysis(aggConPercentChart, branchConPercentChart, aggEntryValChart, branchEntryValChart, oneToAllEntryChart, allToAllEntryChart);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === '1') {
            aggConPercentChart.style.display = "";
            branchConPercentChart.style.display = "none";
        } else {
            aggConPercentChart.style.display = "none";
            branchConPercentChart.style.display = "";
        }
    });
}
if (urlType === '2') {
    showTitleAnalysis(titleTwo, titleOne, titleThree);
    showChartAnalysis(aggEntryValChart, aggConPercentChart, branchConPercentChart, branchEntryValChart, oneToAllEntryChart, allToAllEntryChart);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === '1') {
            aggEntryValChart.style.display = "";
            branchEntryValChart.style.display = "none";
        } else {
            aggEntryValChart.style.display = "none";
            branchEntryValChart.style.display = "";
        }
    });
}
if (urlType === '3') {
    showTitleAnalysis(titleThree, titleOne, titleTwo);
    showChartAnalysis(allToAllEntryChart, oneToAllEntryChart, branchEntryValChart, aggEntryValChart, branchConPercentChart, aggConPercentChart);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === '1') {
            allToAllEntryChart.style.display = "";
            oneToAllEntryChart.style.display = "none";
        } else {
            allToAllEntryChart.style.display = "none";
            oneToAllEntryChart.style.display = "";
        }
    });
}


