function priceSeparator(str_price) {
    price = Number(str_price).toLocaleString("fa-IR")
    return price
}
const prices = document.querySelectorAll(".price");
document.addEventListener("DOMContentLoaded", () => {
    prices.forEach((price) => {
        price.innerHTML = priceSeparator(price.innerHTML);
    });
})