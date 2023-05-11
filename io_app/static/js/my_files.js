function showFileInfoModal(modalID, filename, size, extension, uuid, upload_date,
                           download_url, remove_url, preview_url) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("modal-file-name").innerHTML = filename;

    document.getElementById("modal-file-uuid").innerHTML = uuid;
    document.getElementById("modal-file-size").innerHTML = size + "MB";
    document.getElementById("modal-file-extension").innerHTML = extension;
    document.getElementById("modal-file-date").innerHTML = upload_date;

    document.getElementById("modal-file-download").action = download_url;
    document.getElementById("modal-file-remove").action = remove_url;
    document.getElementById("modal-file-preview").href = preview_url;

    document.getElementById("modal-remove-file-name").innerHTML = filename;

    modal.show();
}