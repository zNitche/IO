function createDoughnutGraph(graphId, data, displayLegend=false) {
    const graphContainer = document.getElementById(graphId);

    let graphCanvas = document.createElement("canvas");
    graphCanvas.id = graphId;

    graphContainer.appendChild(graphCanvas);

    let legend = {display: false}

    if (displayLegend) {
        legend = {
            position: "top",
            labels: {
                color: "#fff",
                font: {
                    size: 15,
                }
            }
          }
    }

    const graphConfig = {
      type: "doughnut",
      data: data,
      options: {
        responsive: true,
        plugins: {
            legend: legend
        },
        animation: {
            duration: 0
        }
      },
    };

    new Chart(graphCanvas.getContext("2d"), graphConfig)
}