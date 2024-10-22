window.onload = function () {
    // Main stock price chart
    var chart = new CanvasJS.Chart("chartContainer", {
        animationEnabled: true,
        theme: "dark1",
        title: {
            text: "Stock Price Data",
            fontColor: "#00FF00"
        },
        axisX: {
            valueFormatString: "DD MMM",
            labelFontColor: "#00FF00",
            crosshair: {
                enabled: true,
                snapToDataPoint: true
            }
        },
        axisY: {
            title: "Closing Price (in USD)",
            valueFormatString: "$##0.00",
            labelFontColor: "#00FF00",
            crosshair: {
                enabled: true,
                snapToDataPoint: true,
                labelFormatter: function (e) {
                    return "$" + CanvasJS.formatNumber(e.value, "##0.00");
                }
            }
        },
        data: [{
            type: "area",
            xValueFormatString: "DD MMM",
            yValueFormatString: "$##0.00",
            color: "#00FF00",
            dataPoints: []  // Data will be loaded dynamically
        }]
    });

    document.getElementById("fetchStock").addEventListener("click", function () {
        var symbol = document.getElementById("stockSymbol").value.toUpperCase();
        fetchStockData(symbol, chart);
    });

    function fetchStockData(symbol, chart) {
        fetch(`/get_stock_data/?symbol=${symbol}`)
            .then(response => response.json())
            .then(data => {
                const dataPoints = data.map(point => ({
                    x: new Date(point.x),
                    y: point.y
                }));
                chart.options.data[0].dataPoints = dataPoints;
                chart.render();
                updateStockInfo(symbol);
            })
            .catch(error => console.error('Error fetching stock data:', error));
    }

    function updateStockInfo(symbol) {
        fetch(`/stock_detail/?symbol=${symbol}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById("stock-name").textContent = data.name || symbol;
                document.getElementById("stock-price").textContent = `$${data.current_price || 'N/A'}`;
                document.getElementById("stock-change").textContent = `${data.price_change || 'N/A'} (${data.price_change_percent || 'N/A'}%)`;
                document.getElementById("stock-previous-close").textContent = `Previous Close: $${data.previous_close || 'N/A'}`;
                document.getElementById("stock-volume").textContent = `Volume: ${data.volume || 'N/A'}`;
                document.getElementById("stock-cap").textContent = `Market Cap: $${data.market_cap || 'N/A'}`;
                document.getElementById("stock-pe-ratio").textContent = `P/E Ratio: ${data.pe_ratio || 'N/A'}`;
            })
            .catch(error => console.error('Error fetching stock details:', error));
    }

    document.getElementById("saveStock").addEventListener("click", function () {
        var symbol = document.getElementById("stockSymbol").value.toUpperCase();
        if (symbol) {
            saveStock(symbol);
        } else {
            alert('Please enter a stock symbol.');
        }
    });

    function saveStock(symbol) {
        const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch('/save_stock/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({ stock_symbol: symbol })
        })
        .then(response => {
            if (response.ok) {
                alert('Stock saved successfully!');
            } else {
                alert('Error saving stock.');
            }
        })
        .catch(error => {
            console.error('Error saving stock:', error);
            alert('Error saving stock.');
        });
    }

    // Function to draw Sensex and Nifty charts with similar formatting
    function drawSmallCharts() {
        // Fetch and render Sensex chart
        fetch('/get_sensex_data/')
            .then(response => response.json())
            .then(data => {
                const sensexDataPoints = data.map(point => ({
                    x: new Date(point.x),
                    y: point.y
                }));

                var sensexChart = new CanvasJS.Chart("sensexChartContainer", {
                    theme: "dark1",
                    animationEnabled: true,
                    title: {
                        text: "Sensex",
                        fontColor: "#00FF00"
                    },
                    axisX: {
                        valueFormatString: "DD MMM",
                        labelFontColor: "#00FF00",
                        crosshair: {
                            enabled: true,
                            snapToDataPoint: true
                        }
                    },
                    axisY: {
                        title: "Value",
                        labelFontColor: "#00FF00",
                        crosshair: {
                            enabled: true,
                            snapToDataPoint: true,
                            labelFormatter: function (e) {
                                return CanvasJS.formatNumber(e.value, "##0.00");
                            }
                        }
                    },
                    data: [{
                        type: "line",
                        color: "#FF4500",  // Red for Sensex
                        xValueFormatString: "DD MMM",
                        yValueFormatString: "##0.00",
                        dataPoints: sensexDataPoints
                    }]
                });
                sensexChart.render();
            })
            .catch(error => console.error('Error fetching Sensex data:', error));

        // Fetch and render Nifty chart
        fetch('/get_nifty_data/')
            .then(response => response.json())
            .then(data => {
                const niftyDataPoints = data.map(point => ({
                    x: new Date(point.x),
                    y: point.y
                }));

                var niftyChart = new CanvasJS.Chart("niftyChartContainer", {
                    theme: "dark1",
                    animationEnabled: true,
                    title: {
                        text: "Nifty",
                        fontColor: "#00FF00"
                    },
                    axisX: {
                        valueFormatString: "DD MMM",
                        labelFontColor: "#00FF00",
                        crosshair: {
                            enabled: true,
                            snapToDataPoint: true
                        }
                    },
                    axisY: {
                        title: "Value",
                        labelFontColor: "#00FF00",
                        crosshair: {
                            enabled: true,
                            snapToDataPoint: true,
                            labelFormatter: function (e) {
                                return CanvasJS.formatNumber(e.value, "##0.00");
                            }
                        }
                    },
                    data: [{
                        type: "line",
                        color: "#4169E1",  // Blue for Nifty
                        xValueFormatString: "DD MMM",
                        yValueFormatString: "##0.00",
                        dataPoints: niftyDataPoints
                    }]
                });
                niftyChart.render();
            })
            .catch(error => console.error('Error fetching Nifty data:', error));
    }

    // Draw the Sensex and Nifty charts when the page loads
    drawSmallCharts();
};
