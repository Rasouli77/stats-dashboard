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

aiButtons.forEach(element => {
    element.addEventListener('click', () => {
    aiModal.style.display = 'flex';
    aiLoading.style.display = 'flex';
    aiResponse.style.display = 'none';
    setTimeout(() => {
    aiLoading.style.display = 'none';
    aiResponse.style.display = 'block';
    typeWriter("هوش مصنوعی بزودی به سیستم اضافه می شود.");
    }, 3000);
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