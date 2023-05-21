async function renderRunningProcesses() {
    const apiData = await getData("/api/processes/currently_running");
    const processesData = apiData.processes_data;

    const processesContainer = document.getElementById("processes-wrapper");
    processesContainer.innerHTML = "";

    if (processesData.length > 0) {
        for (let data of processesData) {
            let processContainer = createProcessDetails(data);
            processesContainer.appendChild(processContainer);
        }
    }
}


function createProcessDetails(processData) {
    let container = document.createElement("div");
    container.classList.add("content-wrapper");

    let processTitle = document.createElement("h3");
    processTitle.innerHTML = processData.process_name;

    let detailsContainer = document.createElement("div");
    detailsContainer.classList.add("file-details-wrapper");

    detailsContainer.appendChild(processTitle);

    let detailsWrapper = document.createElement("span");

    for (attr in processData) {
        let detailsWrapper = document.createElement("span");

        detailsWrapper.innerHTML = `<b>${attr}:</b> ${processData[attr]}`;
        detailsContainer.appendChild(detailsWrapper);
    }

    container.appendChild(detailsContainer);

    return container;
}
