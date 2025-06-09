let nodes = [];
let edges = [];
let network;

function gerarMapa() {
  const pontos = document.getElementById("pontos").value;

  fetch("/api/mapa", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pontos: parseInt(pontos) })
  })
  .then(res => res.json())
  .then(data => {
    nodes = new vis.DataSet(data.nodes.map((n, i) => ({ id: n, label: n })));
    edges = new vis.DataSet(data.edges.map(e => ({
      from: e.from,
      to: e.to,
      label: `${e.weight} min`,
      font: { align: "top" }
    })));

    const container = document.getElementById("graph");
    const options = {
      edges: {
        arrows: "to",
        smooth: false
      },
      physics: {
        enabled: true,
        stabilization: false
      }
    };

    network = new vis.Network(container, { nodes, edges }, options);
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
    if (data.erro) {
      alert(data.erro);
      return;
    }

    const rota = data.rota;
    edges.forEach(edge => {
      edge.color = "#ccc";
      edge.width = 1;
    });

    rota.forEach(([from, to]) => {
      edges.update({
        id: `${from}-${to}`,
        from,
        to,
        color: { color: "red" },
        width: 4
      });
    });

    alert(`Melhor rota leva ${data.tempo_total} minutos.`);
  });
}
