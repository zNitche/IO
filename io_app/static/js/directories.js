function showDirectoryInfoModal(modalID, name, uuid, size, files_count, creation_date) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("modal-directory-name").innerHTML = name;

    document.getElementById("modal-directory-uuid").innerHTML = uuid;
    document.getElementById("modal-directory-size").innerHTML = size + "MB";
    document.getElementById("modal-directory-files").innerHTML = files_count;
    document.getElementById("modal-directory-date").innerHTML = creation_date;

    document.getElementById("modal-directory-download").action = "#";
    document.getElementById("modal-directory-preview").href = `/directories/${uuid}/`;
    document.getElementById("modal-directory-management").href = `/storage/directories/${uuid}/management`;

    modal.show();
}
