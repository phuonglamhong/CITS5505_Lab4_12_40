/*
Competitor dashboard functionality.

This file handles:
- Brand filtering
- API data fetching
- Dynamic summary rendering
- Dynamic chart rendering
*/

let chart;

// Filter displayed brands using search input. 
function filterBrands() {
    const query = document.getElementById('brand-search').value.toLowerCase();

    document.querySelectorAll('.brand-row').forEach(row => {

        const name = row.dataset.brand.toLowerCase();

        row.style.display = name.includes(query)
            ? ''
            : 'none';
    });
}

// Render competitor sentiment chart. 
function loadChart(data) {

    const ctx = document.getElementById('competitorChart');

    const labels = data.map(b => b.name);
    const positive = data.map(b => b.pos);
    const neutral = data.map(b => b.neu);
    const negative = data.map(b => b.neg);

    // Destroy existing chart before re-rendering
    if (chart) {
        chart.destroy();
    }

    chart = new Chart(ctx, {

        type: 'bar',

        data: {
            labels: labels,

            datasets: [
                {
                    label: 'Positive',
                    data: positive,
                    backgroundColor: 'green'
                },
                {
                    label: 'Neutral',
                    data: neutral,
                    backgroundColor: 'gold'
                },
                {
                    label: 'Negative',
                    data: negative,
                    backgroundColor: 'red'
                }
            ]
        },

        options: {
            responsive: true,
            maintainAspectRatio: false
        }
    });
}


// Render summary table dynamically.
function renderSummary(data) {

    const summary = document.getElementById('summary-body');

    summary.innerHTML = '';

    data.forEach(b => {

        summary.innerHTML += `

      <tr>

        <td>${b.name}</td>

        <td>${b.score}</td>

        <td>${b.articles}</td>

        <td>${b.neg}%</td>

      </tr>
    `;
    });
}

// Fetch competitor data from backend API.
function loadData() {

    fetch('/api/competitors')

        .then(response => response.json())

        .then(data => {

            renderBrands(data);

            renderSummary(data);

            loadChart(data);
        });
}

// Load competitor data after page loads.
document.addEventListener(
    'DOMContentLoaded',
    loadData
);