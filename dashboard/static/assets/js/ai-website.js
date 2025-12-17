// AI Buttons
const containerBarChartToolsAI = document.querySelector('#container-bar-chart-tools .ai');
const containerToolsAI = document.querySelector("#container-tools .ai");
const visitsBarChartToolsAI = document.querySelector('#visits-bar-chart-tools .ai');
const visitsToolsAI = document.querySelector("#visits-tools .ai");
const bounceBarChartToolsAI = document.querySelector('#bounce-bar-chart-tools .ai');
const bounceToolsAI = document.querySelector("#bounce-tools .ai");
const timeBarChartToolsAI = document.querySelector('#time-bar-chart-tools .ai');
const timeToolsAI = document.querySelector("#time-tools .ai");
const countBarChartToolsAI = document.querySelector('#count-bar-chart-tools .ai');
const countToolsAI = document.querySelector("#count-tools .ai");
const amountBarChartToolsAI = document.querySelector('#amount-bar-chart-tools .ai');
const amountToolsAI = document.querySelector("#amount-tools .ai");
const productBarChartToolsAI = document.querySelector('#product-bar-chart-tools .ai');
const productToolsAI = document.querySelector("#product-tools .ai");

// AI UI Modal Components
const aiModal = document.getElementById('aiModal');
const aiClose = document.getElementById('aiClose');
const aiLoading = document.getElementById('aiLoading');
const aiResponse = document.getElementById('aiResponse');

// AI Response
let answer = '';

// AI Sent Data
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
const apiUrl = "/api/ai-website";

// Button List
const aiButtons = [
    containerBarChartToolsAI,
    containerToolsAI,
    visitsBarChartToolsAI,
    visitsToolsAI,
    bounceBarChartToolsAI,
    bounceToolsAI,
    countBarChartToolsAI,
    countToolsAI,
    timeToolsAI,
    timeBarChartToolsAI,
    amountBarChartToolsAI,
    amountToolsAI,
    productBarChartToolsAI,
    productToolsAI
]

async function ai_response(e, a, startDate, endDate) {
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
        })
    });
    const data = await response.json();
    return data.ai
}
    

aiButtons.forEach(element => {
    element.addEventListener('click', async () => {
    console.log(aiStartDate, aiEndDate, csrftoken);
    console.log(element.parentElement.id)
    aiModal.style.display = 'flex';
    aiLoading.style.display = 'flex';
    aiResponse.style.display = 'none';
    try {
        // traffic
        if (element.parentElement.id === 'container-bar-chart-tools' || element.parentElement.id === 'container-tools') {
            answer = await ai_response('traffic', true, aiStartDate, aiEndDate); 
        }
        // visits
        if (element.parentElement.id === 'visits-bar-chart-tools' || element.parentElement.id === 'visits-tools') {
            answer = await ai_response('visits', true, aiStartDate, aiEndDate); 
        }
        // bounce
        if (element.parentElement.id === 'bounce-bar-chart-tools' || element.parentElement.id === 'bounce-tools') {
            answer = await ai_response('bounce rate', true, aiStartDate, aiEndDate); 
        }
        // avg time spent
        if (element.parentElement.id === 'time-bar-chart-tools' || element.parentElement.id === 'time-tools') {
            answer = await ai_response('average time spent', true, aiStartDate, aiEndDate); 
        }
        // count
        if (element.parentElement.id === 'count-bar-chart-tools' || element.parentElement.id === 'count-tools') {
            answer = await ai_response('invoice count', true, aiStartDate, aiEndDate); 
        }
        // amount
        if (element.parentElement.id === 'amount-bar-chart-tools' || element.parentElement.id === 'amount-tools') {
            answer = await ai_response('invoice amount', true, aiStartDate, aiEndDate); 
        }
        // product
        if (element.parentElement.id === 'product-bar-chart-tools' || element.parentElement.id === 'product-tools') {
            answer = await ai_response('products sold', true, aiStartDate, aiEndDate); 
        }
        aiLoading.style.display = 'none';
        aiResponse.style.display = 'block';
        console.log(aiResponse);
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