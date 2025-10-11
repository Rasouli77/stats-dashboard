// Initialize
const currentURL = window.location.href;
const parsedURL = new URL(currentURL);
const urlType = parsedURL.searchParams.get("type");
// Titles
const titleOne = document.getElementById("title-type-1");
const titleTwo = document.getElementById("title-type-2");
const titleThree = document.getElementById("title-type-3");
const titleFour = document.getElementById("title-type-4");
// Display Toggle
const displayToggle = document.getElementById("chart-display-toggle");
// TCR
const aggConPercentChart = document.getElementById("ratio-container");
const aggConPercentChartTools = document.getElementById("ratio-container-tools");
// TCR Bar Chart
const cratioContainerBarChart = document.getElementById("ratio-container-bar-chart");
const cratioContainerBarChartTools = document.getElementById("ratio-container-bar-chart-tools");
// BTCR
const branchConPercentChart = document.getElementById("ratio-container-multi-branch");
const branchConPercentChartTools = document.getElementById("ratio-container-multi-branch-tools");
// BTCR Pie Chart
const branchConPercentPieChart = document.getElementById("ratio-container-multi-branch-pie-chart");
const branchConPercentPieChartTools = document.getElementById("ratio-container-multi-branch-pie-chart-tools");
// EV
const aggEntryValChart = document.getElementById("second-ratio-container");
const aggEntryValChartTools = document.getElementById("second-ratio-container-tools");
// EV Bar Chart
const aggEntryValBarChart = document.getElementById("second-ratio-container-bar-chart");
const aggEntryValBarChartTools = document.getElementById("second-ratio-container-bar-chart-tools");
// BEV
const branchEntryValChart = document.getElementById("second-ratio-container-multi-branch");
const branchEntryValChartTools = document.getElementById("second-ratio-container-multi-branch-tools");
// BEV Pie Chart
const branchEntryValPieChart = document.getElementById("second-ratio-container-multi-branch-pie-chart");
const branchEntryValPieChartTools = document.getElementById("second-ratio-container-multi-branch-pie-chart-tools");
// BTS
const oneToAllEntryChart =  document.getElementById("one-to-all-container");
const oneToAllEntryChartTools =  document.getElementById("one-to-all-container-tools");
// BTS Bar Chart
const oneToAllEntryBarChart =  document.getElementById("one-to-all-container-bar-chart");
const oneToAllEntryBarChartTools =  document.getElementById("one-to-all-container-bar-chart-tools");
// TBTS
const allToAllEntryChart = document.getElementById("second-one-to-all-container");
const allToAllEntryChartTools = document.getElementById("second-one-to-all-container-tools");
// TBTS Pie Chart
const allToAllEntryPieChart = document.getElementById("second-one-to-all-container-pie-chart");
const allToAllEntryPieChartTools = document.getElementById("second-one-to-all-container-pie-chart-tools");
// IPB
const cproductCounter = document.getElementById("product-counter");
const cproductCounterTools = document.getElementById("product-counter-tools");
// IPB Bar Chart
const cproductCounterBarChart = document.getElementById("product-counter-bar-chart");
const cproductCounterBarChartTools = document.getElementById("product-counter-bar-chart-tools");
// BIPB
const productCounterBranch = document.getElementById("product-counter-branch");
const productCounterBranchTools = document.getElementById("product-counter-branch-tools");
// BIPB Pie Chart
const productCounterBranchPieChart = document.getElementById("product-counter-branch-pie-chart");
const productCounterBranchPieChartTools = document.getElementById("product-counter-branch-pie-chart-tools");

// Title Display Function
function showTitleAnalysis(one, two, three, four) {
    // one is always dispalyed
    one.style.display = "block";
    // The rest are hidden
    two.style.display = "none";
    three.style.display = "none";
    four.style.display = "none";
}   
// Elements For Url 1
const typeOneList = [
    cratioContainerBarChart,
    cratioContainerBarChartTools,
]
const typeOneListToggleTwo = [
    branchConPercentPieChart,
    branchConPercentPieChartTools
]
const typeOneListToggleTwoLine = [
    aggConPercentChart,
    aggConPercentChartTools,
    branchConPercentChart,
    branchConPercentChartTools,
]
// Elements For Url 2
const typeTwoList = [
    aggEntryValBarChart,
    aggEntryValBarChartTools,
]
const typeTwoListToggleTwo = [
    branchEntryValPieChart,
    branchEntryValPieChartTools
]
const typeTwoListToggleTwoLine = [
    aggEntryValChart,
    aggEntryValChartTools,
    branchEntryValChart,
    branchEntryValChartTools,
]
// Elements For Url 3
const typeThreeList = [
    oneToAllEntryBarChart,
    oneToAllEntryBarChartTools,
]
const typeThreeListToggleTwo = [
    allToAllEntryPieChart,
    allToAllEntryPieChartTools,
]
const typeThreeListToggleTwoLine = [
    oneToAllEntryChart,
    oneToAllEntryChartTools,
    allToAllEntryChart,
    allToAllEntryChartTools,
]
// Elements For Url 4
const typeFourList = [
    cproductCounterBarChart,
    cproductCounterBarChartTools,
]
const typeFourListToggleTwo = [
    productCounterBranchPieChart,
    productCounterBranchPieChartTools
]
const typeFourListToggleTwoLine = [
    productCounterBranch,
    productCounterBranchTools,
    cproductCounter,
    cproductCounterTools,
]
function showOneUrlGroup(listOne, listTwo, listThree, listFour) {
    // shows all the elements
    listOne.forEach(element => {
        element.style.display = "";
    });
    // hides the rest
    const otherLists = [listTwo, listThree, listFour]
    otherLists.forEach(list => {
        list.forEach(element => {
            element.style.display = "none";
        });
    });
}

// Chart Type Display Toggles
function chartTypeToggle(buttonQueryString, hideOne, hideTwo, showOne, showTwo) {
    const button = document.querySelector(buttonQueryString);
    button.addEventListener("click", () => {
        document.getElementById(hideOne).style.display = "none";
        document.getElementById(hideTwo).style.display = "none";
        document.getElementById(showOne).style.display = "";
        document.getElementById(showTwo).style.display = "";
    });
}
const chartToggleItems = [
    ["#ratio-container-tools .bar-chart", "ratio-container-tools", "ratio-container", "ratio-container-bar-chart-tools", "ratio-container-bar-chart"],
    ["#ratio-container-bar-chart-tools .line-chart", "ratio-container-bar-chart", "ratio-container-bar-chart-tools", "ratio-container", "ratio-container-tools"],
    ["#ratio-container-multi-branch-tools .pie-chart", "ratio-container-multi-branch-tools", "ratio-container-multi-branch", "ratio-container-multi-branch-pie-chart", "ratio-container-multi-branch-pie-chart-tools"],
    ["#ratio-container-multi-branch-pie-chart-tools .line-chart", "ratio-container-multi-branch-pie-chart", "ratio-container-multi-branch-pie-chart-tools", "ratio-container-multi-branch", "ratio-container-multi-branch-tools"],
    ["#second-ratio-container-tools .bar-chart", "second-ratio-container", "second-ratio-container-tools", "second-ratio-container-bar-chart", "second-ratio-container-bar-chart-tools"],
    ["#second-ratio-container-bar-chart-tools .line-chart", "second-ratio-container-bar-chart", "second-ratio-container-bar-chart-tools", "second-ratio-container", "second-ratio-container-tools"],
    ["#second-ratio-container-multi-branch-tools .pie-chart", "second-ratio-container-multi-branch", "second-ratio-container-multi-branch-tools", "second-ratio-container-multi-branch-pie-chart", "second-ratio-container-multi-branch-pie-chart-tools"],
    ["#second-ratio-container-multi-branch-pie-chart-tools .line-chart", "second-ratio-container-multi-branch-pie-chart", "second-ratio-container-multi-branch-pie-chart-tools", "second-ratio-container-multi-branch", "second-ratio-container-multi-branch-tools"],
    ["#one-to-all-container-tools .bar-chart", "one-to-all-container", "one-to-all-container-tools", "one-to-all-container-bar-chart", "one-to-all-container-bar-chart-tools"],
    ["#one-to-all-container-bar-chart-tools .line-chart", "one-to-all-container-bar-chart", "one-to-all-container-bar-chart-tools", "one-to-all-container", "one-to-all-container-tools"],
    ["#second-one-to-all-container-tools .pie-chart", "second-one-to-all-container", "second-one-to-all-container-tools", "second-one-to-all-container-pie-chart", "second-one-to-all-container-pie-chart-tools"],
    ["#second-one-to-all-container-pie-chart-tools .bar-chart", "second-one-to-all-container-pie-chart", "second-one-to-all-container-pie-chart-tools", "second-one-to-all-container", "second-one-to-all-container-tools"],
    ["#product-counter-tools .bar-chart", "product-counter", "product-counter-tools", "product-counter-bar-chart", "product-counter-bar-chart-tools"],
    ["#product-counter-bar-chart-tools .line-chart", "product-counter-bar-chart", "product-counter-bar-chart-tools", "product-counter", "product-counter-tools"],
    ["#product-counter-branch-tools .pie-chart", "product-counter-branch", "product-counter-branch-tools", "product-counter-branch-pie-chart", "product-counter-branch-pie-chart-tools"],
    ["#product-counter-branch-pie-chart-tools .line-chart", "product-counter-branch-pie-chart", "product-counter-branch-pie-chart-tools", "product-counter-branch", "product-counter-branch-tools"],
]

chartToggleItems.forEach(list => {
    chartTypeToggle(...list);
});

if (urlType === '1') {
    showTitleAnalysis(titleOne, titleTwo, titleThree, titleFour);
    showOneUrlGroup(typeOneList, typeTwoList, typeThreeList, typeFourList);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === "1") {
        typeOneList.forEach(element => {
            element.style.display = "";
        });
        typeOneListToggleTwo.forEach(element => {
            element.style.display = "none";
        });
        typeOneListToggleTwoLine.forEach(element => {
            element.style.display = "none";
        });
        } else {
            typeOneList.forEach(element => {
                element.style.display = "none";
            });
            typeOneListToggleTwo.forEach(element => {
                element.style.display = "";
            });
            typeOneListToggleTwoLine.forEach(element => {
            element.style.display = "none";
            });
        }
    });  
}
if (urlType === '2') {
    showTitleAnalysis(titleTwo, titleOne, titleThree, titleFour);
    showOneUrlGroup(typeTwoList, typeOneList, typeThreeList, typeFourList);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === "1") {
        typeTwoList.forEach(element => {
            element.style.display = "";
        });
        typeTwoListToggleTwo.forEach(element => {
            element.style.display = "none";
        });
        typeTwoListToggleTwoLine.forEach(element => {
            element.style.display = "none";
        });
        } else {
            typeTwoList.forEach(element => {
                element.style.display = "none";
            });
            typeTwoListToggleTwo.forEach(element => {
                element.style.display = "";
            });
            typeTwoListToggleTwoLine.forEach(element => {
            element.style.display = "none";
            });
        }
    }); 
}
if (urlType === '3') {
    showTitleAnalysis(titleThree, titleOne, titleTwo, titleFour);
    showOneUrlGroup(typeThreeList, typeOneList, typeTwoList, typeFourList);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === "1") {
        typeThreeList.forEach(element => {
            element.style.display = "";
        });
        typeThreeListToggleTwo.forEach(element => {
            element.style.display = "none";
        });
        typeThreeListToggleTwoLine.forEach(element => {
            element.style.display = "none";
        });
        } else {
            typeThreeList.forEach(element => {
                element.style.display = "none";
            });
            typeThreeListToggleTwo.forEach(element => {
                element.style.display = "";
            });
            typeThreeListToggleTwoLine.forEach(element => {
            element.style.display = "none";
            });
        }
    }); 
}
if (urlType === '4') {
    showTitleAnalysis(titleFour, titleOne, titleTwo, titleThree);
    showOneUrlGroup(typeFourList, typeOneList, typeTwoList, typeThreeList);
    displayToggle.addEventListener("change", () => {
        if (displayToggle.value === "1") {
        typeFourList.forEach(element => {
            element.style.display = "";
        });
        typeFourListToggleTwo.forEach(element => {
            element.style.display = "none";
        });
        typeFourListToggleTwoLine.forEach(element => {
            element.style.display = "none";
        });
        } else {
            typeFourList.forEach(element => {
                element.style.display = "none";
            });
            typeFourListToggleTwo.forEach(element => {
                element.style.display = "";
            });
            typeFourListToggleTwoLine.forEach(element => {
            element.style.display = "none";
            });
        }
    }); 
}







