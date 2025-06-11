const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");

let nodes = [];
let edges = [];
let rotaAtual = [];
let eventoAtual = "Nenhum evento.";
let tempoTotal = 0;

const padding = 60;
const nodeRadius = 10;

const cores = {
    node: "#7d4ba3",
    nodeHover: "#bb8de7",
    edgeNormal: "#9b7cd4",
    edgeModerado: "#e07ab7",
    edgeExtremo: "#d63f7b",
    rota: "#ff69b4",
    texto: null,
};

let scale = 1;
let offsetX = 0;
let offsetY = 0;
let isDragging = false;
let dragStart = { x: 0, y: 0 };

const tooltip = document.createElement("div");
tooltip.className = "tooltip";
document.body.appendChild(tooltip);

function setColorsByTheme() {
    const isDark = document.body.classList.contains("dark-mode");
    cores.texto = isDark ? "#d8b8f0" : "#4b006e";
}
setColorsByTheme();

function transformarCoordenadas(x, y) {
    const scaleX = (canvas.width - 2 * padding) / 150;
    const scaleY = (canvas.height - 2 * padding) / 150;

    return {
        x: padding + (x * scaleX) * scale * 1 + offsetX,
        y: canvas.height - (padding + (y * scaleY) * scale) + offsetY,
    };
}

function inversoCoordenadas(canvasX, canvasY) {
    const scaleX = (canvas.width - 2 * padding) / 150;
    const scaleY = (canvas.height - 2 * padding) / 150;

    let x = (canvasX - padding - offsetX) / (scaleX * scale);
    let y = (canvas.height - canvasY + offsetY - padding) / (scaleY * scale);
    return { x, y };
}

function desenharMapa() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    edges.forEach(({ from, to, congestion, weight }) => {
        const fromNode = nodes.find(n => n.id === from);
        const toNode = nodes.find(n => n.id === to);
        if (!fromNode || !toNode) return;

        const p1 = transformarCoordenadas(fromNode.x, fromNode.y);
        const p2 = transformarCoordenadas(toNode.x, toNode.y);

        let corAresta = cores.edgeNormal;
        if (congestion > 0.7) corAresta = cores.edgeExtremo;
        else if (congestion > 0.3) corAresta = cores.edgeModerado;

        let isNaRota = false;
        for (let i = 0; i < rotaAtual.length - 1; i++) {
            const n1 = rotaAtual[i];
            const n2 = rotaAtual[i + 1];
            if ((n1 === from && n2 === to) || (n1 === to && n2 === from)) {
                isNaRota = true;
                break;
            }
        }

        ctx.strokeStyle = isNaRota ? cores.rota : corAresta;
        ctx.lineWidth = isNaRota ? 4 : 2;
        ctx.lineCap = "round";

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();

        // Peso e congestionamento
        const midX = (p1.x + p2.x) / 2;
        const midY = (p1.y + p2.y) / 2;

        ctx.fillStyle = cores.texto;
        ctx.font = "11px 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        const textoPeso = weight.toFixed(1);
        const textoCongest = congestion > 0 ? `(${(congestion * 100).toFixed(0)}%)` : "";
        ctx.fillText(`${textoPeso} ${textoCongest}`, midX + 6, midY - 6);
    });

    nodes.forEach(({ id, x, y }) => {
        const p = transformarCoordenadas(x, y);

        const naRota = rotaAtual.includes(id);
        ctx.fillStyle = naRota ? cores.rota : cores.node;
        ctx.strokeStyle = naRota ? "#a70075" : "#4b006e";
        ctx.lineWidth = 2;

        ctx.beginPath();
        ctx.arc(p.x, p.y, nodeRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.fillStyle = cores.texto;
        ctx.font = "13px 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
        ctx.textAlign = "center";
        ctx.textBaseline = "bottom";
        ctx.fillText(id, p.x, p.y - nodeRadius - 10);
    });
}

function mostrarTooltip(text, x, y) {
    tooltip.textContent = text;
    tooltip.style.left = x + 15 + "px";
    tooltip.style.top = y + 15 + "px";
    tooltip.classList.add("visible");
}

function esconderTooltip() {
    tooltip.classList.remove("visible");
}

function getNodeUnderMouse(mouseX, mouseY) {
    for (const node of nodes) {
        const p = transformarCoordenadas(node.x, node.y);
        const dx = mouseX - p.x;
        const dy = mouseY - p.y;
        if (Math.sqrt(dx * dx + dy * dy) <= nodeRadius + 5) {
            return node;
        }
    }
    return null;
}

function getEdgeUnderMouse(mouseX, mouseY) {
    for (const edge of edges) {
        const fromNode = nodes.find(n => n.id === edge.from);
        const toNode = nodes.find(n => n.id === edge.to);
        if (!fromNode || !toNode) continue;

        const p1 = transformarCoordenadas(fromNode.x, fromNode.y);
        const p2 = transformarCoordenadas(toNode.x, toNode.y);

        const dist = distanciaPontoLinha(mouseX, mouseY, p1.x, p1.y, p2.x, p2.y);
        if (dist < 6) {
            return edge;
        }
    }
    return null;
}

function distanciaPontoLinha(px, py, x1, y1, x2, y2) {
    const A = px - x1;
    const B = py - y1;
    const C = x2 - x1;
    const D = y2 - y1;

    const dot = A * C + B * D;
    const len_sq = C * C + D * D;
    let param = -1;
    if (len_sq !== 0) param = dot / len_sq;

    let xx, yy;
    if (param < 0) {
        xx = x1;
        yy = y1;
    } else if (param > 1) {
        xx = x2;
        yy = y2;
    } else {
        xx = x1 + param * C;
        yy = y1 + param * D;
    }

    const dx = px - xx;
    const dy = py - yy;
    return Math.sqrt(dx * dx + dy * dy);
}

canvas.addEventListener("wheel", (e) => {
    e.preventDefault();

    const delta = e.deltaY > 0 ? 0.9 : 1.1;
    scale *= delta;
    scale = Math.min(Math.max(scale, 0.6), 3);

    draw();
});

canvas.addEventListener("mousedown", (e) => {
    isDragging = true;
    dragStart.x = e.clientX - offsetX;
    dragStart.y = e.clientY - offsetY;
    canvas.style.cursor = "grabbing";
});

canvas.addEventListener("mouseup", () => {
    isDragging = false;
    canvas.style.cursor = "grab";
});

canvas.addEventListener("mouseleave", () => {
    isDragging = false;
    canvas.style.cursor = "grab";
});

canvas.addEventListener("mousemove", (e) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = e.clientX - rect.left;
    const mouseY = e.clientY - rect.top;

    if (isDragging) {
        offsetX = e.clientX - dragStart.x;
        offsetY = e.clientY - dragStart.y;
        draw();
        esconderTooltip();
    } else {
        const nodeHover = getNodeUnderMouse(mouseX, mouseY);
        if (nodeHover) {
            mostrarTooltip(`Nó: ${nodeHover.id}`, e.clientX, e.clientY);
            return;
        }
        const edgeHover = getEdgeUnderMouse(mouseX, mouseY);
        if (edgeHover) {
            mostrarTooltip(
                `Aresta: ${edgeHover.from} → ${edgeHover.to}\nPeso: ${edgeHover.weight.toFixed(
                    2
                )}\nCongestionamento: ${(edgeHover.congestion * 100).toFixed(0)}%`,
                e.clientX,
                e.clientY
            );
            return;
        }
        esconderTooltip();
    }
});

document.getElementById("resetViewBtn").addEventListener("click", () => {
    scale = 1;
    offsetX = 0;
    offsetY = 0;
    draw();
});

async function carregarMapa() {
    try {
        const response = await fetch("/api/mapa");
        if (!response.ok) throw new Error("Erro na resposta do servidor");
        const data = await response.json();

        nodes = data.nodes;
        edges = data.edges;

        preencherSelects();
        draw();
    } catch (err) {
        alert("Erro ao carregar mapa.");
        console.error(err);
    }
}

function preencherSelects() {
    const origemSelect = document.getElementById("origem");
    const destinoSelect = document.getElementById("destino");

    origemSelect.innerHTML = "";
    destinoSelect.innerHTML = "";

    nodes.forEach(({ id }) => {
        const optionOrigem = document.createElement("option");
        optionOrigem.value = id;
        optionOrigem.textContent = id;
        origemSelect.appendChild(optionOrigem);

        const optionDestino = document.createElement("option");
        optionDestino.value = id;
        optionDestino.textContent = id;
        destinoSelect.appendChild(optionDestino);
    });

    if (nodes.length > 1) {
        origemSelect.value = nodes[0].id;
        destinoSelect.value = nodes[nodes.length - 1].id;
    }
}

async function calcularRota() {
    const origem = document.getElementById("origem").value;
    const destino = document.getElementById("destino").value;
    const prioridade = document.getElementById("prioridade").value;

    if (origem === destino) {
        alert("Origem e destino devem ser diferentes.");
        return;
    }

    try {
        const res = await fetch("/api/rota", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ origem, destino, prioridade }),
        });

        if (!res.ok) {
            alert("Erro ao comunicar com servidor.");
            return;
        }

        const data = await res.json();

        if (data.success && Array.isArray(data.rota)) {
            rotaAtual = data.rota;
            tempoTotal = typeof data.tempo === "number" ? data.tempo : 0;
            eventoAtual = data.evento || "Nenhum evento.";
            draw();
            mostrarDetalhesRota();
        } else {
            alert("Erro ao calcular rota: " + (data.error || "Resposta inválida"));
        }
    } catch (err) {
        alert("Erro na comunicação com o servidor.");
        console.error(err);
    }
}

function mostrarDetalhesRota() {
    const detalhesEl = document.getElementById("detalhesRota");
    if (!rotaAtual.length) {
        detalhesEl.textContent = "Nenhuma rota calculada ainda.";
        return;
    }

    let texto = `Rota calculada (${rotaAtual.length} nós):\n`;
    texto += rotaAtual.join(" → ") + "\n\n";
    texto += `Tempo total estimado: ${tempoTotal.toFixed(2)} minutos\n\n`;
    texto += `Evento imprevisto: ${eventoAtual}`;
    detalhesEl.textContent = texto;
}

document.getElementById("calcularBtn").addEventListener("click", calcularRota);

document.getElementById("toggleThemeBtn").addEventListener("click", () => {
    const body = document.body;
    const btn = document.getElementById("toggleThemeBtn");

    if (body.classList.contains("light-mode")) {
        body.classList.remove("light-mode");
        body.classList.add("dark-mode");
        btn.textContent = "☀️";
    } else {
        body.classList.remove("dark-mode");
        body.classList.add("light-mode");
        btn.textContent = "🌙";
    }
    setColorsByTheme();
    draw();
});

function draw() {
    desenharMapa();
}

carregarMapa();
