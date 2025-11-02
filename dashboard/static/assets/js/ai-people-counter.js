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

// AI Response
let answer = '';

// AI Sent Data
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const apiUrl = "/api/ai";

// Button List
const aiButtons = [
    containerBarChartToolsAI,
    containerToolsAI,
    secondContainerPieChartToolsAI,
    secondContainerToolsAI
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
        if (element.parentElement.id === 'container-bar-chart-tools' || element.parentElement.id === 'container-tools') {
            answer = await ai_response('traffic', true, aiStartDate, aiEndDate, aiBranchIds); 
        } 
        if (element.parentElement.id === 'second-container-tools' || element.parentElement.id === 'second-container-pie-chart-tools') {
            answer = await ai_response('traffic', false, aiStartDate, aiEndDate, aiBranchIds); 
        }
        aiLoading.style.display = 'none';
        aiResponse.style.display = 'block';
        typeWriter(answer);
    } catch (error) {
        console.error(error);
        aiLoading.style.display = 'none';
        aiResponse.style.display = 'block';
        answer = "خطایی رخ داده. اتصال به اینترنت را بررسی کنید";
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