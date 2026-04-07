function createConfusionMatrix(canvasId, values) {

    const ctx = document.getElementById(canvasId).getContext("2d");
    const max = Math.max(...values);

    const data = {
        datasets: [{
            data: [
                {x: 0, y: 0, v: values[0]},
                {x: 1, y: 0, v: values[1]},
                {x: 0, y: 1, v: values[2]},
                {x: 1, y: 1, v: values[3]}
            ],
            backgroundColor(ctx) {
                const value = ctx.dataset.data[ctx.dataIndex].v;
                const max = 80860;
                const intensity = value / max;
                return `rgba(0, ${150 + 100 * intensity}, 255, 0.9)`;
            },
            hoverBackgroundColor(ctx) {
                const value = ctx.dataset.data[ctx.dataIndex].v;
                const max = 80860;
                const intensity = value / max;
                return `rgba(0, ${180 + 75 * intensity}, 255, 1)`; // léger effet hover
            },
            borderWidth: 2,
            borderRadius: 5,
            borderColor: "white",
            width: (ctx) => {
                const chart = ctx.chart;
                const area = chart.chartArea;
                if (!area) return 0; // important !
                return area.width / 2*0.9; // 2 colonnes
            },
            height: (ctx) => {
                const chart = ctx.chart;
                const area = chart.chartArea;
                if (!area) return 0; // important !
                return area.height / 2*0.9; // 2 lignes
            },
        

        }]
    };

    // Plugin affichage des valeurs
    const valueLabelsPlugin = {
        id: 'valueLabels',
        afterDatasetsDraw(chart) {
            const { ctx } = chart;

            chart.data.datasets.forEach((dataset, i) => {
                const meta = chart.getDatasetMeta(i);

                meta.data.forEach((element, index) => {
                    const d = dataset.data[index];
                    const { x, y, width, height } = element.getProps(['x', 'y', 'width', 'height'], true);

                    ctx.fillStyle = "white";
                    ctx.font = "16px Arial";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "middle";

                    ctx.fillText(d.v, x + width / 2, y + height / 2);
                });
            });
        }

    };

    new Chart(ctx, {
        type: "matrix",
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false // supprime le titre + carré
                },
                tooltip: {
                    enabled: false // supprime le texte au hover
                }
            },
            scales: {
                x: {
                    ticks: { 
                        callback: (v) => ["PREDIT 0", "PREDIT 1"][v],
                        color: "#ABABAB"
                    },
                    offset: false,
                    grid: { display: false },
                    min: -0.5,
                    max: 1.5,
                    categoryPercentage: 1,
                    barPercentage: 1
                },
                y: {
                    ticks: { 
                        callback: (v) => ["REEL 0", "REEL 1"][v], 
                        color: "#ABABAB"
                    },
                    offset: false,
                    grid: { display: false },
                    min: -0.5,
                    max: 1.5,
                    categoryPercentage: 1,
                    barPercentage: 1
                }
            }
        },
        plugins: [valueLabelsPlugin]
    });

};
