const returnBtn = document.getElementById("return");
const menuTwo = document.getElementById("menu");
const body = document.getElementById("body");
const titleOne = document.getElementById("title-type-1");
const titleTwo = document.getElementById("title-type-2");
const titleThree = document.getElementById("title-type-3");
const titleFour = document.getElementById("title-type-4");
const titleFive = document.getElementById("title-type-5");
const titleSix = document.getElementById("title-type-6");

// Return Button
returnBtn.addEventListener("click", () => {
    menuTwo.style.display = "block";
    body.style.display = "none";
    returnBtn.style.display = "none";
});
// Selected Branches
let selectedBranchesChecks = 0;
document.querySelectorAll(".form-check-input").forEach((el) => {
    if (el.checked === true) {
        selectedBranchesChecks += 1;
    }
});
// TCR
// Card
const aggConPercentCard = document.getElementById("agg-con-percent");
// Chart
const aggConPercentChart = document.getElementById("ratio-container");

// BTCR
// Card
const branchConPercentCard = document.getElementById("branch-con-percent");
// Chart
const branchConPercentChart = document.getElementById("ratio-container-multi-branch");

// EV
// Card
const aggEntryValCard = document.getElementById("agg-entry-val");
// Chart
const aggEntryValChart = document.getElementById("second-ratio-container");

// BEV
// Card
const branchEntryValCard = document.getElementById("branch-entry-val");
// Chart
const branchEntryValChart = document.getElementById("second-ratio-container-multi-branch");

// BTS
// Card
const oneToAllEntryCard = document.getElementById("one-to-all-entry");
// Chart
const oneToAllEntryChart =  document.getElementById("one-to-all-container");

// TBTS
// Card
const allToAllEntryCard = document.getElementById("all-to-all-entry");
// Chart
const allToAllEntryChart = document.getElementById("second-one-to-all-container");

function showTitleAnalysis(one, two, three, four, five, six) {
    // one is always dispalyed
    one.style.display = "block";
    // The rest are hidden
    two.style.display = "none";
    three.style.display = "none";
    four.style.display = "none";
    five.style.display = "none";
    six.style.display = "none";
}

// First Card
aggConPercentCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "block";
    branchConPercentChart.style.display = "none";
    aggEntryValChart.style.display = "none";
    branchEntryValChart.style.display = "none";
    oneToAllEntryChart.style.display = "none";
    allToAllEntryChart.style.display = "none";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleOne, titleTwo, titleThree, titleFour, titleFive, titleSix);
});

// Second Card
branchConPercentCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "none";
    branchConPercentChart.style.display = "block";
    aggEntryValChart.style.display = "none";
    branchEntryValChart.style.display = "none";
    oneToAllEntryChart.style.display = "none";
    allToAllEntryChart.style.display = "none";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleTwo, titleOne, titleThree, titleFour, titleFive, titleSix);
});

// Third Card
aggEntryValCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "none";
    branchConPercentChart.style.display = "none";
    aggEntryValChart.style.display = "block";
    branchEntryValChart.style.display = "none";
    oneToAllEntryChart.style.display = "none";
    allToAllEntryChart.style.display = "none";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleThree, titleOne, titleTwo, titleFour, titleFive, titleSix);
});

// Forth Card
branchEntryValCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "none";
    branchConPercentChart.style.display = "none";
    aggEntryValChart.style.display = "none";
    branchEntryValChart.style.display = "block";
    oneToAllEntryChart.style.display = "none";
    allToAllEntryChart.style.display = "none";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleFour, titleOne, titleTwo, titleThree, titleFive, titleSix);
});

// Fifth Card
oneToAllEntryCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "none";
    branchConPercentChart.style.display = "none";
    aggEntryValChart.style.display = "none";
    branchEntryValChart.style.display = "none";
    oneToAllEntryChart.style.display = "block";
    allToAllEntryChart.style.display = "none";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleFive, titleOne, titleTwo, titleThree, titleFour, titleSix);
});

// Sixth Card
allToAllEntryCard.addEventListener("click", () => {
    menuTwo.style.display = "none";
    body.style.display = "block";
    aggConPercentChart.style.display = "none";
    branchConPercentChart.style.display = "none";
    aggEntryValChart.style.display = "none";
    branchEntryValChart.style.display = "none";
    oneToAllEntryChart.style.display = "none";
    allToAllEntryChart.style.display = "block";
    returnBtn.style.display = "block";
    showTitleAnalysis(titleSix, titleOne, titleTwo, titleThree, titleFour, titleFive);
});