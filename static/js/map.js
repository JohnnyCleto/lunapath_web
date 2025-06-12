document.addEventListener("DOMContentLoaded", () => {
    const origemSelect = document.getElementById("origem");
    const destinoSelect = document.getElementById("destino");
    const calcularBtn = document.getElementById("calcular");
    const statusP = document.getElementById("status");
    const custoP = document.getElementById("custo");
    const rotaAltP = document.getElementById("rota-alternativa");
    const canvas = document.getElementById("mapa");
    const ctx = canvas.getContext("2d");

    let locais = [];
    let posicoes = {};
    let arestas = [];
    let rotaAtual = [];
    let zoom = 4;
    let offsetX = 0;
    let offsetY = 0;
    let isDragging = false;
    let dragStart = {x: 0, y: 0};
    let offsetStart = {x: 0, y: 0};

    // Preenche selects de locais
    async function carregarLocais() {
        const res = await fetch("/api/locais");
        locais = await res.json();
        for (const local of locais) {
            let opt1 = document.createElement("option");
            opt1.value = local;
            opt1.textContent = local;
            origemSelect.appendChild(opt1);

            let opt2 = document.createElement("option");
            opt2.value = local;
            opt2.textContent = local;
            destinoSelect.appendChild(opt2);
        }
        // Defaults para teste rápido
        origemSelect.value = "Casa de Luna";
        destinoSelect.value = "Plataforma de Lançamento Espacial";
    }

    // Converte coordenadas do grafo para canvas
    function coordParaTela(x, y) {
        return {
            x: (x * zoom) + offsetX,
            y: (y * zoom) + offsetY,
        };
    }

    // Desenha o mapa e a rota
    function desenharMapa() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);

        // Desenha arestas (ruas)
        for (const a of arestas) {
            const p1 = coordParaTela(...posicoes[a.u]);
            const p2 = coordParaTela(...posicoes[a.v]);

            // Cor baseada em congestionamento ou bloqueio
            if (a.blocked) {
                ctx.strokeStyle = "red";
                ctx.lineWidth = 3;
                ctx.setLineDash([8, 8]);
            } else if (a.congestion > 1.2) {
                ctx.strokeStyle = `rgba(255,165,0,${Math.min((a.congestion-1)/2,1)})`; // laranja com intensidade
                ctx.lineWidth = 2;
                ctx.setLineDash([]);
            } else {
                ctx.strokeStyle = "#999";
                ctx.lineWidth = 1;
                ctx.setLineDash([]);
            }

            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }

        // Desenha nós
        for (const local of locais) {
            const pos = coordParaTela(...posicoes[local]);
            ctx.beginPath();
            ctx.arc(pos.x, pos.y, 7, 0, 2 * Math.PI);
            if (rotaAtual.includes(local)) {
                ctx.fillStyle = "#1a73e8";
                ctx.shadowColor = "#1a73e8";
                ctx.shadowBlur = 10;
            } else {
                ctx.fillStyle = "#444";
                ctx.shadowBlur = 0;
            }
            ctx.fill();
            ctx.shadowBlur = 0;

            // Texto dos locais
            ctx.font = "12px Arial";
            ctx.fillStyle = (document.body.classList.contains("dark-mode")) ? "#eee" : "#222";
            ctx.fillText(local, pos.x + 10, pos.y + 5);
        }

        // Desenha rota (linhas azuis grossas)
        if (rotaAtual.length > 1) {
            ctx.strokeStyle = "#1a73e8";
            ctx.lineWidth = 4;
            ctx.setLineDash([]);
            ctx.beginPath();
            for (let i = 0; i < rotaAtual.length - 1; i++) {
                const p1 = coordParaTela(...posicoes[rotaAtual[i]]);
                const p2 = coordParaTela(...posicoes[rotaAtual[i + 1]]);
                if (i === 0) ctx.moveTo(p1.x, p1.y);
                ctx.lineTo(p2.x, p2.y);
            }
            ctx.stroke();
        }
    }

    // Atualiza rota via API
    async function atualizarRota() {
        const origem = origemSelect.value;
        const destino = destinoSelect.value;

        if (origem === destino) {
            statusP.textContent = "Origem e destino não podem ser iguais.";
            return;
        }

        statusP.textContent = "Calculando rota...";
        rotaAltP.hidden = true;
        custoP.textContent = "";

        const res = await fetch("/api/rota", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({origem, destino}),
        });

        if (!res.ok) {
            const err = await res.json();
            statusP.textContent = "Erro: " + err.error;
            return;
        }

        const dados = await res.json();
        rotaAtual = dados.caminho;
        posicoes = dados.posicoes;
        arestas = dados.arestas;
        custoP.textContent = `Distância estimada: ${dados.custo.toFixed(2)} unidades`;
        if (dados.rota_alternativa) {
            rotaAltP.hidden = false;
        }
        statusP.textContent = `Rota calculada de ${origem} até ${destino}`;
        desenharMapa();
    }

    // Zoom in/out via roda do mouse
    canvas.addEventListener("wheel", (e) => {
        e.preventDefault();
        const zoomAmount = e.deltaY * -0.01;
        zoom = Math.min(Math.max(1, zoom + zoomAmount), 20);
        desenharMapa();
    });

    // Drag para mover mapa
    canvas.addEventListener("mousedown", (e) => {
        isDragging = true;
        dragStart = {x: e.clientX, y: e.clientY};
        offsetStart = {x: offsetX, y: offsetY};
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
        if (isDragging) {
            offsetX = offsetStart.x + (e.clientX - dragStart.x);
            offsetY = offsetStart.y + (e.clientY - dragStart.y);
            desenharMapa();
        }
    });

    // Alternar modo claro/escuro e salvar no localStorage
    const toggleBtn = document.getElementById("toggle-theme");
    function aplicarTema(escuro) {
        if (escuro) {
            document.body.classList.add("dark-mode");
        } else {
            document.body.classList.remove("dark-mode");
        }
        desenharMapa();
    }
    toggleBtn.addEventListener("click", () => {
        const escuro = !document.body.classList.contains("dark-mode");
        aplicarTema(escuro);
        localStorage.setItem("temaEscuro", escuro);
    });
    // Aplica tema salvo ao carregar
    const temaSalvo = localStorage.getItem("temaEscuro") === "true";
    aplicarTema(temaSalvo);

    calcularBtn.addEventListener("click", atualizarRota);

    carregarLocais();
});
