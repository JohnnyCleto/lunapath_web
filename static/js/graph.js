let network, nodes, edges, locais = [];

fetch("/api/mapa")
  .then(res => res.json())
  .then(data => {
    locais = data.nodes.map(n => n.label);
    const origemSelect = document.getElementById("origem");
    const destinoSelect = document.getElementById("destino");

    locais.forEach(loc => {
      origemSelect.innerHTML += `<option>${loc}</option>`;
      destinoSelect.innerHTML += `<option>${loc}</option>`;
    });

    nodes = new vis.DataSet(data.nodes.map(n => ({
      id: n.id,
      label: n.label,
      x: n.x * 100,
      y: n.y * 100,
      fixed: true
    })));

    edges = new vis.DataSet(data.edges.map((e, i) => ({
      id: `${e.from}-${e.to}`,
      from: e.from,
      to: e.to,
      label: `${e.weight} min`,
      font: { align: "top" },
      arrows: "to"
    })));

    const container = document.getElementById("graph");
    const options = { physics: false };
    network = new vis.Network(container, { nodes, edges }, options);
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

    edges.forEach(edge => edges.update({ id: edge.id, color: "#ccc", width: 1 }));

    data.rota.forEach(([from, to]) => {
      const id = `${from}-${to}`;
      edges.update({ id, color: { color: "red" }, width: 4 });
    });

    alert(`Tempo total: ${data.tempo_total} minutos`);
  });
}
