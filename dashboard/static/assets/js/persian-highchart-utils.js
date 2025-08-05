const observer = new MutationObserver(() => {
    const buttons = document.querySelectorAll(".highcharts-menu-item");
    const listContainer = document.querySelector(".highcharts-menu");
    if (buttons.length >= 5) {
        buttons[2].style.display = 'none';
        buttons[3].style.display = 'none';
        buttons[4].style.display = 'none';
        buttons[0].textContent = 'نمایش تمام صفحه';
        buttons[1].textContent = 'PDF خروجی';
        buttons[5].textContent = 'CSV خروجی';
        buttons[6].textContent = 'XLS خروجی';
        buttons[7].textContent = 'نمایش جدول';
        observer.disconnect();
    }
});


observer.observe(document.body, {
    childList: true,
    subtree: true
});   