const returnBtn = document.getElementById("return");
const menuTwo = document.getElementById("menu");
const body = document.getElementById("body");
const campaigns = document.querySelector("#campaigns");
const groupedCampaigns = document.querySelector("#grouped-campaigns");
const instruction = document.getElementById("instruction");
const instructionForOneToAllContainer = document.getElementById("instruction-for-one-to-all-container");

// Return Button
returnBtn.addEventListener("click", () => {
    menuTwo.style.display = "block";
    body.style.display = "none";
    returnBtn.style.display = "none";
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
    campaigns.style.display = "none";
    groupedCampaigns.style.display = "block";
    instruction.style.display = "none";
    instructionForOneToAllContainer.style.display = "none";
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
    if (branchConPercentChart.childNodes.length === 0) {
        campaigns.style.display = "none";
    } else {
        campaigns.style.display = "block";
    }
    groupedCampaigns.style.display = "none";
    instruction.style.display = "block";
    instructionForOneToAllContainer.style.display = "none";
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
    campaigns.style.display = "none";
    groupedCampaigns.style.display = "block";
    instruction.style.display = "none";
    instructionForOneToAllContainer.style.display = "none";
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
    campaigns.style.display = "block";
    groupedCampaigns.style.display = "none";
    instruction.style.display = "block";
    instructionForOneToAllContainer.style.display = "none";
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
    campaigns.style.display = "none";
    groupedCampaigns.style.display = "block";
    instruction.style.display = "none";
    instructionForOneToAllContainer.style.display = "block";
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
    campaigns.style.display = "block";
    groupedCampaigns.style.display = "none";
    instruction.style.display = "block";
    instructionForOneToAllContainer.style.display = "none";
});