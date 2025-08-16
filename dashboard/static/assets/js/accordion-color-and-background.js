document.querySelectorAll(".accordion-button")[0].addEventListener("click", () => {
    if (document.querySelector("#collapseDate").querySelector(".selected")) {
        document.querySelectorAll(".accordion-button")[0].style.color = "#5a8dee";
        document.querySelectorAll(".accordion-button")[0].style.boxShadow = "0 0.25rem 1rem rgba(147, 158, 170, 0.45)";
    }
})

document.querySelectorAll(".accordion-button")[1].addEventListener("click", () => {
    let checked = false;
    document.querySelectorAll(".fake-check").forEach((e) => {
        if (e.checked === true) {
            checked = true;
        }
    });
    if (checked === true) {
        document.querySelectorAll(".accordion-button")[1].style.color = "#5a8dee";
        document.querySelectorAll(".accordion-button")[1].style.boxShadow = "0 0.25rem 1rem rgba(147, 158, 170, 0.45)";
    } else {
        document.querySelectorAll(".accordion-button")[1].style.color = "";
        document.querySelectorAll(".accordion-button")[1].style.boxShadow = "";
    }
})