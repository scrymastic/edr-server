
document.addEventListener('DOMContentLoaded', function() {
    function renderChart(elementId, type) {
        var canvas = document.getElementById(elementId);
        if (canvas) {
            var chartData = JSON.parse(canvas.getAttribute('data-chart'));
            var ctx = canvas.getContext('2d');
            
            new Chart(ctx, {
                type: type,
                data: chartData,
                options: getChartOptions(type)
            });
        }
    }

    function getChartOptions(type) {
        if (type === 'doughnut') {
            return {
                responsive: true,
                maintainAspectRatio: false,
                circumference: 180,
                rotation: -90,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Alert Severity Distribution'
                    }
                },
                layout: {
                    padding: {
                        top: 10,
                        bottom: 10
                    }
                }
            };
        } else if (type === 'bar') {
            return {
                indexAxis: 'y',
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: 'Event Type Distribution'
                    }
                },
                scales: {
                    x: {
                        beginAtZero: true,
                        title: {
                            display: true,
                            text: 'Count'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Event Type'
                        }
                    }
                }
            };
        }
    }

    renderChart('alertChart', 'doughnut');
    renderChart('eventsChart', 'bar');
});