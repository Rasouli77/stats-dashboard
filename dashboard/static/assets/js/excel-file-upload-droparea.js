const dragarea = document.querySelector("#dragarea");
const excelFile = document.querySelector("#excel_file");
const dropzone = document.querySelector("#dropzone-basic");
const submitInvoiceUpload = document.querySelector("#submit-invoice-upload");
const removeFile = document.querySelector("#remove-invoice-file");
removeFile.classList.add("hidden");
dragarea.addEventListener("click", () => {excelFile.click()});
excelFile.addEventListener("change", () => {
    dragarea.innerHTML = `<i class='menu-icon tf-icons bx bx-file'></i> ${excelFile.files[0].name}`
    removeFile.classList.remove("hidden");
});
dragarea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropzone.classList.add("dragover");
});
dragarea.addEventListener("dragleave", () => {
    dropzone.classList.remove("dragover");
});
dragarea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropzone.classList.remove("dragover");
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        excelFile.files = files;
        dragarea.innerHTML = `<i class='menu-icon tf-icons bx bx-file'></i> ${excelFile.files[0].name}`
        removeFile.classList.remove("hidden");
    }
});
submitInvoiceUpload.addEventListener("click", () => {dropzone.submit()});
removeFile.addEventListener("click", () => {location.reload()});