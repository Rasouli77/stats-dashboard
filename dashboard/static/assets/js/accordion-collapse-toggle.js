const accordionButton = document.querySelector(".accordion-button");
const collapseDate = document.getElementById("collapseDate");
const accordionCollapse = document.querySelector(".accordion-collapse");
const collapseBranch = document.getElementById("collapseBranch");
document.getElementById('filter-form').addEventListener("click", () => {
    accordionButton.classList.add("collapsed");
    accordionButton.ariaExpanded = false;
    collapseDate.style = "";
    collapseDate.classList.remove("show");
    accordionCollapse.classList.add("collapsed");
    accordionCollapse.ariaExpanded = false;
    collapseBranch.style = "";
    collapseBranch.classList.remove("show");
});
