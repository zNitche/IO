function fallbackToLocalFileLink(el, localPath) {
    el.href = localPath;
}


function fallbackToLocalJS(el, localPath) {
    document.write("<script src=" + localPath + "></script>");
}


async function getData(url) {
    const options = {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        }

    const response = await fetch(url, options);

    return response.json();
}


async function postData(url, data={}) {
    const options = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        }

    const response = await fetch(url, options);

    return response.json();
}


function showModal(modalID) {
    let modal = new bootstrap.Modal(document.getElementById(modalID));

    if (modal) {
        modal.show();
    }
}
