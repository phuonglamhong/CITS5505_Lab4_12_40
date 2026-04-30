/* ============================================================
   competitor.js — Competitor Analysis page logic
   Checkpoint 2: Brand search filter via DOM
   Checkpoint 3: Replace with fetch('/api/competitors')
   ============================================================ */

function filterBrands() {
  const query = document.getElementById('brand-search').value.toLowerCase();
  document.querySelectorAll('.brand-row').forEach(row => {
    const name = row.dataset.brand.toLowerCase();
    row.style.display = name.includes(query) ? '' : 'none';
  });
}

let chart; // global chart variable

function loadChart(data) {
  const ctx = document.getElementById('competitorChart');

  const labels = data.map(b => b.name);
  const positive = data.map(b => b.pos);
  const neutral = data.map(b => b.neu);
  const negative = data.map(b => b.neg);

  if (chart) chart.destroy(); // prevent duplicate chart

  chart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [
        { label: 'Positive', data: positive, backgroundColor: 'green' },
        { label: 'Neutral', data: neutral, backgroundColor: 'gray' },
        { label: 'Negative', data: negative, backgroundColor: 'red' }
      ]
    }
  });
}

// Fetching Backend Data

function loadData() {
  fetch('/api/competitors')
    .then(res => res.json())
    .then(data => {
      renderBrands(data);
      loadChart(data);
    });
}

// Dynamic Rendering

function renderBrands(data) {
  const container = document.getElementById('brand-list');
  container.innerHTML = '';

  data.forEach(b => {
    container.innerHTML += `
      <div class="brand-row" data-brand="${b.name}">
        <div class="brand-name">${b.name}</div>

        <div class="brand-bar-wrap">
          <div class="d-flex" style="height:8px;border-radius:4px;overflow:hidden;">
            <div style="width:${b.pos}%;background:green;"></div>
            <div style="width:${b.neu}%;background:gold;"></div>
            <div style="width:${b.neg}%;background:red;"></div>
          </div>
        </div>

        <div class="brand-score">${b.score}</div>
        <div>${b.articles} arts</div>
      </div>
    `;
  });
}


// Load Data on Page Load

document.addEventListener('DOMContentLoaded', loadData);