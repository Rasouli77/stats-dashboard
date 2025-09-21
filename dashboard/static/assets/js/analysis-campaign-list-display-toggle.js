const returnBtn = document.getElementById("return");
const menuTwo = document.getElementById("menu");
const body = document.getElementById("body");
const groupedCampaigns = document.querySelector("#grouped-campaigns");

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
    groupedCampaigns.style.display = "block";
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
    groupedCampaigns.style.display = "block";
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
    groupedCampaigns.style.display = "block";
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
    groupedCampaigns.style.display = "block";
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
    groupedCampaigns.style.display = "block";
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
    groupedCampaigns.style.display = "block";
});