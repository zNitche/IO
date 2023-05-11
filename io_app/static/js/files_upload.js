function uploadProgressHandler(event) {
    const progressBar = document.getElementById("upload-file-progress");
    const progressValue = document.getElementById("upload-file-progress-value");

    let progress = Math.floor((event.loaded / event.total) * 100);

    progressBar.value = progress;
    progressValue.innerHTML = progress + "%";
}


function uploadFile(upload_url, csrf_token) {
    const xhr = new XMLHttpRequest();
    const file = document.getElementById("file-upload").files[0];

    if (file) {
        toggleFileUploadElements();
        setupFileUploadDetails(file.name);

        xhr.upload.addEventListener("progress", uploadProgressHandler, false);

        xhr.onloadend = function(event) {
            onUploadFinished(event);
        }

        xhr.open("POST", upload_url, true);

        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.setRequestHeader("X-File-Name", file.name);
        xhr.setRequestHeader("X-File-Size", file.size);
        xhr.setRequestHeader("Content-Type", file.type||"application/octet-stream");
        xhr.setRequestHeader("X-CSRFToken", csrf_token);

        xhr.send(file);
    }
}


function onUploadFinished(event) {
    const response = event.currentTarget;
    const message = JSON.parse(response.responseText).message;

    showInfoModal("uploadInfoModal", message);

    hideFileUploadDetailsContainer();
    toggleFileUploadElements();
    postUploadContainer();

    document.getElementById("file-upload").value = null;
}


function onFileSelected(event) {
    const filesInput = event.currentTarget;
    const fileNameWrapper = document.getElementById("upload-file-name-wrapper");

    if (filesInput.files[0]) {
        const filesUploadButton = document.getElementById("upload-button");
        filesUploadButton.classList.remove("disabled");

        fileNameWrapper.classList.remove("d-none");
        fileNameWrapper.innerHTML = filesInput.files[0].name;
    }
}

function postUploadContainer() {
    const filesUploadButton = document.getElementById("upload-button");
    filesUploadButton.classList.add("disabled");

    const fileNameWrapper = document.getElementById("upload-file-name-wrapper");

    fileNameWrapper.classList.add("d-none");
    fileNameWrapper.innerHTML = ""
}

function toggleFileUploadElements() {
    const filesUploadFormWrapper = document.getElementById("file-upload-form-wrapper");

    filesUploadFormWrapper.classList.toggle("d-none");
}


function setupFileUploadDetails(filename) {
    showFileUploadDetailsContainer();
    const filenameContainer = document.getElementById("upload-file-name");
    filenameContainer.innerHTML = filename;
}


function showFileUploadDetailsContainer() {
    const fileUploadDetailsContainer = document.getElementById("file-upload-details-wrapper");
    fileUploadDetailsContainer.classList.remove("d-none")
}


function hideFileUploadDetailsContainer() {
    const fileUploadDetailsContainer = document.getElementById("file-upload-details-wrapper");
    fileUploadDetailsContainer.classList.add("d-none")
}

function showInfoModal(modalID, text) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("upload-info-modal-text").innerHTML = text;
    modal.show();
}
