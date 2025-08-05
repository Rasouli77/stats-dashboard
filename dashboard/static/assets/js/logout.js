buttonLogout = document.getElementById("fake-logout")
form = document.getElementById("logout-form")
buttonLogout.addEventListener("click", () => {
form.submit()
})