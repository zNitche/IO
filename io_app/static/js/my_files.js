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


async function createStorageUsageGraphs() {
    const storageUsageData = await getData("/api/storage_usage");
    const storageUsageByFiletypeData = await getData("/api/storage_usage_by_filetype");

    console.log(storageUsageData)
    console.log(storageUsageByFiletypeData)

    createDoughnutGraph("storage-usage", getDatasetForStorageUsageData(storageUsageData));
    createDoughnutGraph("storage-usage-by-type", getDatasetForStorageUsageByFiletypeData(storageUsageByFiletypeData), false);
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
