function showFileInfoModal(modalID, filename, size, extension, uuid, upload_date, directory_name, directory_url) {
    const management_url_base = `/files/${uuid}`;

    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("modal-file-name").innerHTML = filename;

    document.getElementById("modal-file-uuid").innerHTML = uuid;
    document.getElementById("modal-file-size").innerHTML = size + "MB";
    document.getElementById("modal-file-extension").innerHTML = extension;
    document.getElementById("modal-file-date").innerHTML = upload_date;
    document.getElementById("modal-file-directory").innerHTML = directory_name;

    document.getElementById("modal-file-directory-link").href = directory_url;

    document.getElementById("modal-file-download").action = `${management_url_base}/download/`;
    document.getElementById("modal-file-remove").action = `${management_url_base}/remove/`;
    document.getElementById("modal-file-preview").href = `${management_url_base}/preview/`;

    document.getElementById("modal-remove-file-name").innerHTML = filename;

    modal.show();
}


async function initStorageUsageStats() {
    const storageUsageData = await getData("/api/storage_usage");
    const storageUsageByFiletypeData = await getData("/api/storage_usage_by_filetype");

    createDoughnutGraph("storage-usage", getDatasetForStorageUsageData(storageUsageData));
    document.getElementById("storage-used-space-value").innerHTML = storageUsageData.used_space + "%";

    createDoughnutGraph("storage-usage-by-type", getDatasetForStorageUsageByFiletypeData(storageUsageByFiletypeData));

    setStorageUsageDetails(storageUsageData);
    setStorageUsageByTypeDetails(storageUsageByFiletypeData);

    document.getElementById("storage-usage-data").classList.remove("d-none")
    document.getElementById("storage-usage-data-wrapper").classList.remove("content-wrapper-loading")
    document.getElementById("storage-usage-data-wrapper").classList.add("no-bottom-padding")

    document.getElementById("storage-usage-data-spinner").classList.add("d-none")
}


function setStorageUsageDetails(storageUsageData) {
    document.getElementById("storage-usage-details-used").innerHTML = storageUsageData.free_space + "MB";
    document.getElementById("storage-usage-details-free").innerHTML = storageUsageData.used_space + "MB";
}


function setStorageUsageByTypeDetails(storageUsageData) {
    const container = document.getElementById("storage-usage-details-by-type");

    for (let extension in storageUsageData) {
        let detailItem = document.createElement("p");
        detailItem.innerHTML = `<b>${extension}:</b> ${storageUsageData[extension]}%`

        container.appendChild(detailItem);
    }
}


function getDatasetForStorageUsageData(storageUsageData) {
    const data = {
      labels: ["Free space", "Used space"],
      datasets: [
        {
          data: [storageUsageData.free_space, storageUsageData.used_space],
          borderColor: "#223767",
          backgroundColor: ["#2dd8a3", "#27468c"],
        }
      ]
    };

    return data;
}


function getDatasetForStorageUsageByFiletypeData(storageUsageData) {
    let labels = [];
    let data = [];

    for (let extension in storageUsageData) {
        labels.push(extension);
        data.push(storageUsageData[extension]);
    }

    const graphData = {
      labels: labels,
      datasets: [
        {
          data: data,
          borderColor: "#223767",
          backgroundColor: ['#011f4b', '#03396c', '#005b96', '#6497b1', '#b3cde0', '#251e3e',
           '4a4e4d', '0e9aa7', '2a4d69', '4b86b4'],
        }
      ]
    };

    return graphData;
}
