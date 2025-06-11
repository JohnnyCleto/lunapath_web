document.addEventListener('DOMContentLoaded', () => {
  const svg = document.getElementById('map');
  const tempoTotalEl = document.getElementById('tempoTotal');
  const eventoEl = document.getElementById('evento');
  const descricaoEl = document.getElementById('descricao');
  const ctx = document.getElementById('chart').getContext('2d');
  let chart;

  fetchMapa();
  fetchLocais();


  document.getElementById('refresh').onclick = fetchMapa;
  document.getElementById('calcRota').onclick = calcularRota;
  document.getElementById('themeToggle').onclick = toggleTheme;

  function toggleTheme() {
    document.body.classList.toggle('dark');
    this.textContent = document.body.classList.contains('dark') ? 'Modo Claro' : 'Modo Escuro';
  }

  function fetchMapa() {
    fetch('/api/mapa')
      .then(r => r.json())
      .then(drawMapa)
      .catch(console.error);
  }
function fetchLocais() {
  fetch('/api/mapa')
    .then(res => res.json())
    .then(data => {
      const locais = data.nodes.map(n => ({ id: n.id, label: n.label }));
      const origemSel = document.getElementById('origem');
      const destinoSel = document.getElementById('destino');

      locais.forEach(loc => {
        const opt1 = document.createElement('option');
        opt1.value = loc.id;
        opt1.textContent = loc.label;
        origemSel.appendChild(opt1);

        const opt2 = document.createElement('option');
        opt2.value = loc.id;
        opt2.textContent = loc.label;
        destinoSel.appendChild(opt2);
      });
    });
}

  function drawMapa(data) {
    const { nodes, edges } = data;
    svg.innerHTML = '';
    const padding = 20;
    const xs = nodes.map(n => n.x);
    const ys = nodes.map(n => n.y);
    const minX = Math.min(...xs), maxX = Math.max(...xs);
    const minY = Math.min(...ys), maxY = Math.max(...ys);
    const scaleX = (svg.clientWidth - 2 * padding) / (maxX - minX);
    const scaleY = (svg.clientHeight - 2 * padding) / (maxY - minY);

    function cx(x) { return padding + (x - minX) * scaleX; }
    function cy(y) { return padding + (y - minY) * scaleY; }

    edges.forEach(e => {
      const n1 = nodes.find(n => n.id === e.from);
      const n2 = nodes.find(n => n.id === e.to);
      const line = document.createElementNS('http://www.w3.org/2000/svg','line');
      line.setAttribute('x1', cx(n1.x));
      line.setAttribute('y1', cy(n1.y));
      line.setAttribute('x2', cx(n2.x));
      line.setAttribute('y2', cy(n2.y));
      line.setAttribute('stroke', congestionColor(e.congestion));
      line.setAttribute('stroke-width', 2);
      line.dataset.from = e.from;
      line.dataset.to = e.to;
      svg.appendChild(line);
    });

    nodes.forEach(n => {
      const circle = document.createElementNS('http://www.w3.org/2000/svg','circle');
      circle.setAttribute('cx', cx(n.x));
      circle.setAttribute('cy', cy(n.y));
      circle.setAttribute('r', 5);
      circle.setAttribute('fill', 'var(--svg-node)');
      const text = document.createElementNS('http://www.w3.org/2000/svg','text');
      text.setAttribute('x', cx(n.x) + 7);
      text.setAttribute('y', cy(n.y) + 3);
      text.textContent = n.label;
      text.setAttribute('fill', getComputedStyle(document.body).color);
      text.style.fontSize = '10px';
      svg.appendChild(circle);
      svg.appendChild(text);
    });
  }

  function congestionColor(c) {
    const r = Math.floor(255 * c);
    const g = Math.floor(200 * (1 - c));
    return `rgb(${r}, ${g}, 0)`;
  }

  function calcularRota() {
    const origem = document.getElementById('origem').value;
    const destino = document.getElementById('destino').value;
    const prioridade = document.getElementById('prioridade').value;
    if (!origem || !destino) return alert('Preencha origem e destino.');

    fetch('/api/rota', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ origem, destino, prioridade })
    })
    .then(r => r.json())
    .then(res => {
      if (res.erro) return alert(res.erro);
      tempoTotalEl.textContent = res.tempo_total + ' unidades';
      eventoEl.textContent = res.evento;
      descricaoEl.textContent = res.descricao_evento;
      highlightRota(res.rota);
      plotChart(res.rota);
    })
    .catch(console.error);
  }

  function highlightRota(rota) {
    Array.from(svg.querySelectorAll('line')).forEach(line => {
      if (rota.includes(line.dataset.from) && rota.includes(line.dataset.to)) {
        line.setAttribute('stroke', 'var(--svg-route)');
        line.setAttribute('stroke-width', 4);
      }
    });
  }

  function plotChart(rota) {
    fetch('/api/mapa')
      .then(r => r.json())
      .then(data => {
        const edges = data.edges;
        const values = [];
        for (let i = 0; i < rota.length -1; i++) {
          const u = rota[i], v = rota[i+1];
          const edge = edges.find(e => (e.from===u && e.to===v) || (e.from===v && e.to===u));
          values.push(edge.congestion);
        }
        const labels = rota.slice(1);
        if (chart) chart.destroy();
        chart = new Chart(ctx, {
          type: 'bar',
          data: {
            labels,
            datasets: [{
              label: 'Congestionamento',
              data: values,
              backgroundColor: values.map(v => congestionColor(v)),
            }]
          },
          options: {
            scales: { y: { beginAtZero: true, max:1 } },
            plugins: { legend: { display: false } }
          }
        });
      });
  }
});
