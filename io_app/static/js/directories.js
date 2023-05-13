function showDirectoryInfoModal(modalID, name, uuid, size, files_count,
                                creation_date, download_url, remove_url, preview_url) {

    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("modal-directory-name").innerHTML = name;

    document.getElementById("modal-directory-uuid").innerHTML = uuid;
    document.getElementById("modal-directory-size").innerHTML = size + "MB";
    document.getElementById("modal-directory-files").innerHTML = files_count;
    document.getElementById("modal-directory-date").innerHTML = creation_date;

    document.getElementById("modal-directory-download").action = download_url;
    document.getElementById("modal-directory-remove").action = remove_url;
    document.getElementById("modal-directory-preview").href = preview_url;

    document.getElementById("modal-remove-directory-name").innerHTML = name;

    modal.show();
}
