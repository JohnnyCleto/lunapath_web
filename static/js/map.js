const canvas = document.getElementById("mapCanvas");
const ctx = canvas.getContext("2d");

let nodes = [];
let edges = [];
let rotaAtual = [];
let eventoAtual = "Nenhum evento.";
let tempoTotal = 0;

const padding = 50;
const nodeRadius = 8;

// Cores
const cores = {
    node: "#7d4ba3",
    edgeNormal: "#9b7cd4",
    edgeModerado: "#e07ab7",
    edgeExtremo: "#d63f7b",
    rota: "#ff69b4",
    texto: "#4b006e",
};

async function carregarMapa() {
    const resp = await fetch("/api/mapa");
    const data = await resp.json();
    nodes = data.nodes;
    edges = data.edges;
    popularSelects();
    desenharMapa();
}

function popularSelects() {
    const origemSel = document.getElementById("origem");
    const destinoSel = document.getElementById("destino");

    origemSel.innerHTML = "";
    destinoSel.innerHTML = "";

    nodes.forEach(({ id }) => {
        const opt1 = document.createElement("option");
        opt1.value = id;
        opt1.textContent = id;
        origemSel.appendChild(opt1);

        const opt2 = document.createElement("option");
        opt2.value = id;
        opt2.textContent = id;
        destinoSel.appendChild(opt2);
    });

    // Set default selections
    origemSel.selectedIndex = 0;
    destinoSel.selectedIndex = nodes.length > 1 ? 1 : 0;
}

function transformarCoordenadas(x, y) {
    // Ajusta coords para canvas com padding
    // Assume posições entre 0 e 150 para x e y, escala para canvas
    const scaleX = (canvas.width - 2 * padding) / 150;
    const scaleY = (canvas.height - 2 * padding) / 150;
    return {
        x: padding + x * scaleX,
        y: canvas.height - (padding + y * scaleY), // inverter eixo y para visualização correta
    };
}

function desenharMapa() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Desenhar arestas (edges)
    edges.forEach(({ from, to, congestion, weight }) => {
        const fromNode = nodes.find(n => n.id === from);
        const toNode = nodes.find(n => n.id === to);
        if (!fromNode || !toNode) return;

        const p1 = transformarCoordenadas(fromNode.x, fromNode.y);
        const p2 = transformarCoordenadas(toNode.x, toNode.y);

        // Cor da aresta com base no congestionamento
        let corAresta = cores.edgeNormal;
        if (congestion > 0.7) corAresta = cores.edgeExtremo;
        else if (congestion > 0.3) corAresta = cores.edgeModerado;

        // Se aresta está na rota atual, destacar
        let isNaRota = false;
        for (let i = 0; i < rotaAtual.length - 1; i++) {
            if (
                (rotaAtual[i] === from && rotaAtual[i + 1] === to) ||
                (rotaAtual[i] === to && rotaAtual[i + 1] === from)
            ) {
                isNaRota = true;
                break;
            }
        }

        ctx.strokeStyle = isNaRota ? cores.rota : corAresta;
        ctx.lineWidth = isNaRota ? 4 : 2;

        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();

        // Mostrar peso e congestionamento perto da linha
        const midX = (p1.x + p2.x) / 2;
        const midY = (p1.y + p2.y) / 2;

        ctx.fillStyle = cores.texto;
        ctx.font = "10px Arial";
        const textoPeso = weight.toFixed(1);
        const textoCongest = congestion > 0 ? `(${(congestion*100).toFixed(0)}%)` : "";
        ctx.fillText(`${textoPeso} ${textoCongest}`, midX + 5, midY - 5);
    });

    // Desenhar nós
    nodes.forEach(({ id, x, y }) => {
        const p = transformarCoordenadas(x, y);

        // Se o nó está na rota atual, cor diferente
        const naRota = rotaAtual.includes(id);
        ctx.fillStyle = naRota ? cores.rota : cores.node;
        ctx.beginPath();
        ctx.arc(p.x, p.y, nodeRadius, 0, Math.PI * 2);
        ctx.fill();

        // Texto do nó
        ctx.fillStyle = cores.texto;
        ctx.font = "12px Arial";
        ctx.textAlign = "center";
        ctx.fillText(id, p.x, p.y - nodeRadius - 6);
    });
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
        const resp = await fetch("/api/rota", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ origem, destino, prioridade }),
        });

        const data = await resp.json();

        if (resp.ok) {
            rotaAtual = data.rota;
            tempoTotal = data.tempo_total;
            eventoAtual = data.evento;

            mostrarDetalhesRota();
            desenharMapa();
        } else {
            alert("Erro ao calcular rota: " + data.error);
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

// Inicializa carregando o mapa
carregarMapa();
