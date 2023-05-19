function showFileInfoModal(modalID, filename, size, extension, uuid, upload_date, directory_name, directory_url, can_be_previewed) {
    const management_url_base = `/storage/files/${uuid}`;

    let modal = new bootstrap.Modal(document.getElementById(modalID));

    document.getElementById("modal-file-name").innerHTML = filename;

    document.getElementById("modal-file-size").innerHTML = size + "MB";
    document.getElementById("modal-file-extension").innerHTML = extension;
    document.getElementById("modal-file-date").innerHTML = upload_date;
    document.getElementById("modal-file-directory").innerHTML = directory_name;

    document.getElementById("modal-file-directory-link").href = directory_url;

    document.getElementById("modal-file-download").action = `${management_url_base}/download/`;

    const previewButton = document.getElementById("modal-file-preview");

    if (can_be_previewed) {
        previewButton.classList.remove("d-none");
        previewButton.href = `${management_url_base}/preview/`;
    } else {
        previewButton.classList.add("d-none");
    }

    const managementButton = document.getElementById("modal-file-management");
    if (managementButton) {
        managementButton.href = `${management_url_base}/management/`;
    }

    modal.show();
}


async function initStorageUsageStats() {
    const storageUsageData = await getData("/api/storage_usage");
    const storageUsageByFiletypeData = await getData("/api/storage_usage_by_filetype");

    createDoughnutGraph("storage-usage", getDatasetForStorageUsageData(storageUsageData));
    document.getElementById("storage-used-space-value").innerHTML = storageUsageData.used_space + "%";

    if (storageUsageData.used_space > 0) {
        createDoughnutGraph("storage-usage-by-type", getDatasetForStorageUsageByFiletypeData(storageUsageByFiletypeData));
    }

    setStorageUsageDetails(storageUsageData);
    setStorageUsageByTypeDetails(storageUsageByFiletypeData);

    document.getElementById("storage-usage-data").classList.remove("d-none");
    document.getElementById("storage-usage-data-wrapper").classList.remove("content-wrapper-loading");
    document.getElementById("storage-usage-data-wrapper").classList.add("no-bottom-padding");

    document.getElementById("storage-usage-data-spinner").classList.add("d-none");
}


function setStorageUsageDetails(storageUsageData) {
    document.getElementById("storage-usage-details-used").innerHTML = storageUsageData.used_space + "MB";
    document.getElementById("storage-usage-details-free").innerHTML = storageUsageData.free_space + "MB";
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
      labels: ["Used space", "Free space"],
      datasets: [
        {
          data: [storageUsageData.used_space, storageUsageData.free_space],
          borderColor: "#223767",
          backgroundColor: ["#27468c", "#2dd8a3"],
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
          backgroundColor: ['#fe7a88', '#f44d43', '#f5b015', '#79992c', '#9a64c6', '#1d9ac6',
           '#db7b00', '#0e9aa7', '#2a4d69', '#4b86b4'],
        }
      ]
    };

    return graphData;
}
