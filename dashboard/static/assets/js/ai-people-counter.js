// AI Buttons
const containerBarChartToolsAI = document.querySelector('#container-bar-chart-tools .ai');
const containerToolsAI = document.querySelector("#container-tools .ai");
const secondContainerPieChartToolsAI = document.querySelector("#second-container-pie-chart-tools .ai"); 
const secondContainerToolsAI = document.querySelector("#second-container-tools .ai"); 

// AI UI Modal Components
const aiModal = document.getElementById('aiModal');
const aiClose = document.getElementById('aiClose');
const aiLoading = document.getElementById('aiLoading');
const aiResponse = document.getElementById('aiResponse');

const aiButtons = [
    containerBarChartToolsAI,
    containerToolsAI,
    secondContainerPieChartToolsAI,
    secondContainerToolsAI
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