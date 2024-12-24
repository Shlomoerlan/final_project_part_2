// Load yearly trends
function loadYearlyTrends() {
    fetch('/trends/yearly')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const plotData = JSON.parse(data.data.plot);
                Plotly.newPlot('yearly-plot', plotData.data, plotData.layout);
            } else {
                console.error('Failed to load yearly trends:', data.message);
            }
        })
        .catch(error => console.error('Error loading yearly trends:', error));
}

// Load monthly trends for a specific year
function loadMonthlyTrends(year) {
    fetch(`/trends/monthly/${year}`)
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const plotData = JSON.parse(data.data.plot);
                Plotly.newPlot('monthly-plot', plotData.data, plotData.layout);
            } else {
                console.error('Failed to load monthly trends:', data.message);
            }
        })
        .catch(error => console.error('Error loading monthly trends:', error));
}

// Initialize the plots
document.addEventListener('DOMContentLoaded', function() {
    // Load yearly trends
    loadYearlyTrends();

    // Setup year selector
    const yearSelect = document.getElementById('year-select');
    yearSelect.addEventListener('change', function(e) {
        loadMonthlyTrends(e.target.value);
    });

    // Load initial monthly data
    loadMonthlyTrends(yearSelect.value);
});
