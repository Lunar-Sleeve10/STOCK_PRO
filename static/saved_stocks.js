document.addEventListener('DOMContentLoaded', function () {
    // Loop through each stock and initialize the chart
    const stockCards = document.querySelectorAll('.stock-card');

    stockCards.forEach(card => {
        const symbol = card.querySelector('h3').innerText.split('(')[1].split(')')[0].trim();
        initChart(symbol);
    });
});

// Function to initialize the stock chart using CanvasJS
function initChart(symbol) {
    const chartContainerId = "chartContainer_" + symbol;
    const chart = new CanvasJS.Chart(chartContainerId, {
        theme: "dark1",
        exportEnabled: true,
        title: {
            text: symbol + " Price Data"
        },
        axisX: {
            labelFontColor: "#00FF00"
        },
        axisY: {
            labelFontColor: "#00FF00"
        },
        data: [{
            type: "spline",
            color: "#00FF00",
            dataPoints: []
        }]
    });

    // Show loading message while fetching stock data
    const loadingMessage = document.createElement('p');
    loadingMessage.textContent = 'Loading data...';
    loadingMessage.style.color = "#00FF00"; // Green color for loading message
    document.getElementById(chartContainerId).appendChild(loadingMessage);

    // Fetch stock data for the graph
    fetch(`/get_stock_data/?symbol=${symbol}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            const dataPoints = data.map(point => ({
                x: new Date(point.x),
                y: point.y
            }));
            chart.options.data[0].dataPoints = dataPoints;
            chart.render();
            // Remove loading message after data is loaded
            loadingMessage.remove();
        })
        .catch(error => {
            console.error('Error fetching stock data:', error);
            loadingMessage.textContent = 'Error loading data. Please try again later.';
            loadingMessage.style.color = "red"; // Red color for error message
        });
}

// Function to handle stock deletion
function deleteStock(stock_id) {
    if (confirm("Are you sure you want to delete this stock?")) {
        fetch(`/delete_stock/${stock_id}/`, { method: 'DELETE' })
            .then(response => {
                if (response.ok) {
                    location.reload(); // Reload the page to see the updated list
                } else {
                    alert("Failed to delete stock.");
                }
            })
            .catch(error => {
                console.error("Error deleting stock:", error);
                alert("Failed to delete stock.");
            });
    }
}
