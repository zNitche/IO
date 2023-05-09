function uploadProgressHandler(event) {
    let progress = Math.floor((event.loaded / event.total) * 100);

    console.log(progress + "%");
}


function asyncSendFile(upload_url, csrf_token) {
    const xhr = new XMLHttpRequest();
    const file = document.getElementById("file-input").files[0];

    if (file) {
        xhr.upload.addEventListener("progress", uploadProgressHandler, false);

        xhr.onloadend = function(event) {
            onUploadFinished(event);
        }

        xhr.open("POST", upload_url, true);

        xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
        xhr.setRequestHeader("X-File-Name", file.name);
        xhr.setRequestHeader("Content-Type", file.type||"application/octet-stream");
        xhr.setRequestHeader("X-CSRFToken", csrf_token);

        xhr.send(file);
    }
}


function onUploadFinished(event) {
    const response = event.currentTarget;
    const message = JSON.parse(response.responseText).message;

    alert(message);
}
