let mapa;
let pontos = [];
let arestas = [];

function initMapa() {
  mapa = L.map('mapa').setView([-23.55, -46.63], 13); // SP por padrão
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapa);
}

function gerarMapa() {
  const qtd = parseInt(document.getElementById("pontos").value);

  fetch("/api/mapa", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pontos: qtd })
  })
  .then(res => res.json())
  .then(data => {
    pontos = data.locais;
    arestas = data.arestas;

    document.getElementById("origem").innerHTML = pontos.map(p => `<option>${p}</option>`).join("");
    document.getElementById("destino").innerHTML = pontos.map(p => `<option>${p}</option>`).join("");

    mapa.eachLayer(layer => {
      if (layer instanceof L.Marker || layer instanceof L.Polyline) mapa.removeLayer(layer);
    });

    const marcadores = {};
    pontos.forEach((nome, i) => {
      const lat = -23.5 + Math.random() * 0.1;
      const lng = -46.6 + Math.random() * 0.1;
      marcadores[nome] = L.marker([lat, lng]).addTo(mapa).bindPopup(nome);
    });

    arestas.forEach(({ from, to, weight }) => {
      L.polyline([
        marcadores[from].getLatLng(),
        marcadores[to].getLatLng()
      ], {
        color: "#999",
        weight: 2
      }).addTo(mapa).bindTooltip(`${weight} min`);
    });
  });
}

function calcularRota() {
  const origem = document.getElementById("origem").value;
  const destino = document.getElementById("destino").value;

  fetch("/api/rota", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origem, destino })
  })
  .then(res => res.json())
  .then(data => {
    if (data.erro) return alert(data.erro);

    const rota = data.rota;
    const pontosMap = {};
    mapa.eachLayer(layer => {
      if (layer instanceof L.Marker) {
        pontosMap[layer.getPopup().getContent()] = layer.getLatLng();
      }
    });

    rota.forEach(([from, to]) => {
      L.polyline([
        pontosMap[from],
        pontosMap[to]
      ], {
        color: "red",
        weight: 4
      }).addTo(mapa);
    });

    alert(`🗺️ Melhor rota leva ${data.tempo_total} minutos.`);
  });
}
