let map = L.map('map').setView([0.003, 0.003], 15);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; LunaPath',
}).addTo(map);

let markers = {};
let polylines = [];

fetch("/api/mapa")
  .then(res => res.json())
  .then(data => {
    data.nodes.forEach(n => {
      const marker = L.marker([n.lat, n.lng]).addTo(map).bindPopup(n.id);
      markers[n.id] = marker;

      let option = new Option(n.id, n.id);
      document.getElementById("origem").add(option.cloneNode(true));
      document.getElementById("destino").add(option.cloneNode(true));
    });
  });

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
    if (data.erro) {
      alert(data.erro);
      return;
    }

    // Limpa rotas anteriores
    polylines.forEach(p => map.removeLayer(p));
    polylines = [];

    data.rota.forEach(seg => {
      const polyline = L.polyline([
        [seg.from_coord.lat, seg.from_coord.lng],
        [seg.to_coord.lat, seg.to_coord.lng]
      ], { color: 'red', weight: 5 }).addTo(map);
      polylines.push(polyline);
    });

    alert(`Melhor rota leva ${data.tempo_total} minutos.`);
  });
}
