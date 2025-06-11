const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");
let nodes = [], edges = [], route = [];

let offsetX = 0, offsetY = 0;
let zoom = 1.0;

async function carregarMapa() {
  const res = await fetch("/api/mapa");
  const data = await res.json();
  nodes = data.nodes;
  edges = data.edges;
  preencherSelects();
  desenharMapa();
}

function preencherSelects() {
  const origem = document.getElementById("origem");
  const destino = document.getElementById("destino");
  origem.innerHTML = destino.innerHTML = "";

  for (const node of nodes) {
    const opt = document.createElement("option");
    opt.value = node.id;
    opt.textContent = node.label;
    origem.appendChild(opt.cloneNode(true));
    destino.appendChild(opt.cloneNode(true));
  }
}

function coordenadasCanvas(x, y) {
  return [
    x * 100 * zoom + 50 + offsetX,
    canvas.height - (y * 100 * zoom + 50 + offsetY)
  ];
}

function desenharMapa() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.fillStyle = "#eaeaea";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  // Desenhar arestas
  ctx.strokeStyle = "#aaa";
  ctx.lineWidth = 2;
  for (const edge of edges) {
    const from = nodes.find(n => n.id === edge.from);
    const to = nodes.find(n => n.id === edge.to);
    const [fx, fy] = coordenadasCanvas(from.x, from.y);
    const [tx, ty] = coordenadasCanvas(to.x, to.y);

    ctx.beginPath();
    ctx.moveTo(fx, fy);
    ctx.lineTo(tx, ty);
    ctx.stroke();
  }

  // Desenhar rota
  if (route.length > 1) {
    ctx.strokeStyle = getComputedStyle(document.body).getPropertyValue("--route-color");
    ctx.lineWidth = 4;
    for (let i = 0; i < route.length - 1; i++) {
      const from = nodes.find(n => n.id === route[i]);
      const to = nodes.find(n => n.id === route[i + 1]);
      const [fx, fy] = coordenadasCanvas(from.x, from.y);
      const [tx, ty] = coordenadasCanvas(to.x, to.y);

      ctx.beginPath();
      ctx.moveTo(fx, fy);
      ctx.lineTo(tx, ty);
      ctx.stroke();
    }
  }

  // Desenhar nós
  for (const node of nodes) {
    const [x, y] = coordenadasCanvas(node.x, node.y);
    ctx.beginPath();
    ctx.arc(x, y, 12, 0, 2 * Math.PI);
    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue("--node-color");
    ctx.fill();
    ctx.strokeStyle = "#333";
    ctx.lineWidth = 2;
    ctx.stroke();

    ctx.fillStyle = getComputedStyle(document.body).getPropertyValue("--text-color");
    ctx.font = "12px Roboto";
    ctx.textAlign = "center";
    ctx.fillText(node.label, x, y - 18);
  }
}

async function solicitarRota() {
  const origem = document.getElementById("origem").value;
  const destino = document.getElementById("destino").value;

  if (origem === destino) {
    alert("Selecione origem e destino diferentes.");
    return;
  }

  const res = await fetch("/api/rota", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ origem, destino })
  });

  const data = await res.json();
  route = data.rota;
  desenharMapa();

  const rDiv = document.getElementById("resultado");
  rDiv.innerHTML = `
    <p><strong>🔗 Rota:</strong> ${route.join(" → ")}</p>
    <p><strong>⏱️ Tempo Estimado:</strong> ${data.tempo_total.toFixed(2)} unidades</p>
  `;
}

function reiniciarMapa() {
  route = [];
  desenharMapa();
  document.getElementById("resultado").innerHTML = "";
}

document.getElementById("btnRota").addEventListener("click", solicitarRota);
document.getElementById("btnReset").addEventListener("click", reiniciarMapa);
document.getElementById("toggleTheme").addEventListener("click", () => {
  document.documentElement.classList.toggle("dark");
  localStorage.setItem("theme", document.documentElement.classList.contains("dark") ? "dark" : "light");
});

carregarMapa();
