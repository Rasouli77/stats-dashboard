// AI Buttons
const ratioContainerToolsAI = document.querySelector('#ratio-container-tools .ai');
const ratioContainerBarChartToolsAI = document.querySelector("#ratio-container-bar-chart-tools .ai");
const ratioContainerMultiBranchPieChartToolsAI = document.querySelector("#ratio-container-multi-branch-pie-chart-tools .ai"); 
const ratioContainerMultiBranchToolsAI = document.querySelector("#ratio-container-multi-branch-tools .ai"); 
const secondRatioContainerBarChartToolsAI = document.querySelector("#second-ratio-container-bar-chart-tools .ai"); 
const secondRatioContainerToolsAI = document.querySelector("#second-ratio-container-tools .ai"); 
const secondRatioContainerMultiBranchPieChartToolsAI = document.querySelector("#second-ratio-container-multi-branch-pie-chart-tools .ai"); 
const secondRatioContainerMultiBranchToolsAI = document.querySelector("#second-ratio-container-multi-branch-tools .ai");
const oneToAllContainerBarChartToolsAI = document.querySelector("#one-to-all-container-bar-chart-tools .ai");
const oneToAllContainerToolsAI = document.querySelector("#one-to-all-container-tools .ai");
const secondOneToAllContainerPieChartToolsAI = document.querySelector("#second-one-to-all-container-pie-chart-tools .ai");
const secondOneToAllContainerToolsAI = document.querySelector("#second-one-to-all-container-tools .ai");
const productCounterBarChartToolsAI = document.querySelector("#product-counter-bar-chart-tools .ai");
const productCounterToolsAI = document.querySelector("#product-counter-tools .ai");
const productCounterBranchPieChartToolsAI = document.querySelector("#product-counter-branch-pie-chart-tools .ai");
const productCounterBranchToolsAI = document.querySelector("#product-counter-branch-tools .ai");

// AI UI Modal Components
const aiModal = document.getElementById('aiModal');
const aiClose = document.getElementById('aiClose');
const aiLoading = document.getElementById('aiLoading');
const aiResponse = document.getElementById('aiResponse');

// AI Response
let answer = '';

// AI Sent Data
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const apiUrl = "/api/ai";

const aiButtons = [
    ratioContainerToolsAI,
    ratioContainerBarChartToolsAI,
    ratioContainerMultiBranchPieChartToolsAI,
    ratioContainerMultiBranchToolsAI,
    secondRatioContainerBarChartToolsAI,
    secondRatioContainerToolsAI,
    secondRatioContainerMultiBranchPieChartToolsAI,
    secondRatioContainerMultiBranchToolsAI,
    oneToAllContainerBarChartToolsAI,
    oneToAllContainerToolsAI,
    secondOneToAllContainerPieChartToolsAI,
    secondOneToAllContainerToolsAI,
    productCounterBarChartToolsAI,
    productCounterToolsAI,
    productCounterBranchPieChartToolsAI,
    productCounterBranchToolsAI
]

async function ai_response(e, a, startDate, endDate, branch) {
    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({
            e: e,
            a: a,
            aiStartDate: startDate,
            aiEndDate: endDate,
            aiBranchIds: branch
        })
    });
    const data = await response.json();
    return data.ai
}

aiButtons.forEach(element => {
    element.addEventListener('click', async () => {
    console.log(aiStartDate, aiEndDate, aiBranchIds, csrftoken);
    console.log(element.parentElement.id)
    aiModal.style.display = 'flex';
    aiLoading.style.display = 'flex';
    aiResponse.style.display = 'none';
    try {
        if (element.parentElement.id === 'ratio-container-bar-chart-tools' || element.parentElement.id === 'ratio-container-tools') {
            answer = await ai_response('conversion rate (invoice count divided by traffic of each date * 100)', true, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'ratio-container-multi-branch-pie-chart-tools' || element.parentElement.id === 'ratio-container-multi-branch-tools') {
            answer = await ai_response('conversion rate (invoice count divided by traffic of each date * 100)', false, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'second-ratio-container-bar-chart-tools' || element.parentElement.id === 'second-ratio-container-tools') {
            answer = await ai_response('traffic divided by invoice: value per visit', true, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'second-ratio-container-multi-branch-pie-chart-tools' || element.parentElement.id === 'second-ratio-container-multi-branch-tools') {
            answer = await ai_response('traffic divided by invoice: value per visit', false, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'one-to-all-container-bar-chart-tools' || element.parentElement.id === 'one-to-all-container-tools') {
            answer = await ai_response('traffic', true, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'second-one-to-all-container-pie-chart-tools' || element.parentElement.id === 'second-one-to-all-container-tools') {
            answer = await ai_response('traffic', false, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'product-counter-bar-chart-tools' || element.parentElement.id === 'product-counter-tools') {
            answer = await ai_response('product sold divided by invoice count', true, aiStartDate, aiEndDate, aiBranchIds); 
        }
        if (element.parentElement.id === 'product-counter-branch-pie-chart-tools' || element.parentElement.id === 'product-counter-branch-tools') {
            answer = await ai_response('product sold divided by invoice count', false, aiStartDate, aiEndDate, aiBranchIds); 
        }
        aiLoading.style.display = 'none';
        aiResponse.style.display = 'block';
        typeWriter(answer);
    } catch (error) {
        console.error(error);
        aiLoading.style.display = 'none';
        aiResponse.style.display = 'block';
        answer = "از اتصال خود اطمینان حاصل کنید و یا بازه ای بیشتر از 10 روز انتخاب کنید";
        typeWriter(answer);
    }
    // Close modal
    aiClose.addEventListener('click', () => {
        aiModal.style.display = 'none';
    });

    // Click outside to close
    window.addEventListener('click', (e) => {
        if (e.target === aiModal) {
            aiModal.style.display = 'none';
        }
    });
    });
});

// Typewriter effect
function typeWriter(text) {
    aiResponse.textContent = '';
    let i = 0;
    const speed = 40;
    function typing() {
    if (i < text.length) {
        aiResponse.textContent += text.charAt(i);
        i++;
        setTimeout(typing, speed);
    }
    }
    typing();
}