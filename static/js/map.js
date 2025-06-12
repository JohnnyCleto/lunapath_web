const canvas = document.getElementById("mapa");
const ctx = canvas.getContext("2d");
const origemSelect = document.getElementById("origem");
const destinoSelect = document.getElementById("destino");
const btn = document.getElementById("calcular-rota");
const statusEl = document.getElementById("status-rota");
const eventoEl = document.getElementById("evento-atual");
const custoEl = document.getElementById("custo-rota");
const detalhesEl = document.getElementById("detalhes-rota");
const toggleBtn = document.getElementById("toggle-theme");

let locais = [];
let pos = {};
let grafoSimples = {};
let caminho = [];
let custo = 0;
let tempoEstimado = 0;
let bolaIdx = 0;
let animando = false;
let animId = null;
let evento = null;

function ajustarCanvas() {
  const r = canvas.getBoundingClientRect();
  canvas.width = r.width * window.devicePixelRatio;
  canvas.height = r.height * window.devicePixelRatio;
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
}

async function carregarLocais() {
  const res = await fetch("/api/locais");
  const data = await res.json();
  locais = data.map(([n, p]) => ({ nome: n, pos: p.pos }));
  locais.forEach(l => {
    pos[l.nome] = l.pos;
    ["origem", "destino"].forEach(id => {
      const sel = document.getElementById(id);
      const opt = document.createElement("option");
      opt.value = l.nome;
      opt.textContent = l.nome;
      sel.appendChild(opt);
    });
  });
  if (locais.length > 1) {
    origemSelect.value = locais[0].nome;
    destinoSelect.value = locais[1].nome;
  }
}

function construirGrafo() {
  grafoSimples = {};
  locais.forEach(l => grafoSimples[l.nome] = []);
  locais.forEach(a => {
    locais.forEach(b => {
      if (a.nome !== b.nome) {
        const dx = a.pos[0] - b.pos[0];
        const dy = a.pos[1] - b.pos[1];
        if (Math.hypot(dx, dy) < 35) {
          grafoSimples[a.nome].push(b.nome);
        }
      }
    });
  });
}

function desenhar() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  const pad = 50;
  const xs = locais.map(l => l.pos[0]);
  const ys = locais.map(l => l.pos[1]);
  const mnx = Math.min(...xs);
  const mxx = Math.max(...xs);
  const mny = Math.min(...ys);
  const mxy = Math.max(...ys);
  const sw = canvas.clientWidth - 2 * pad;
  const sh = canvas.clientHeight - 2 * pad;
  const sc = Math.min(sw / (mxx - mnx), sh / (mxy - mny));
  const ox = pad - mnx * sc + (sw - (mxx - mnx) * sc) / 2;
  const oy = pad - mny * sc + (sh - (mxy - mny) * sc) / 2;
  const proj = (x, y) => [x * sc + ox, y * sc + oy];

  locais.forEach(l => {
    grafoSimples[l.nome].forEach(v => {
      const a = proj(...pos[l.nome]);
      const b = proj(...pos[v]);
      ctx.strokeStyle = "#999";
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.moveTo(...a);
      ctx.lineTo(...b);
      ctx.stroke();
    });
  });

  if (caminho.length > 1) {
    ctx.strokeStyle = "#007acc";
    ctx.lineWidth = 4;
    ctx.beginPath();
    caminho.forEach((n, i) => {
      if (i === 0) ctx.moveTo(...proj(...pos[n]));
      else ctx.lineTo(...proj(...pos[n]));
    });
    ctx.stroke();
  }

  locais.forEach(l => {
    const [x, y] = proj(...pos[l.nome]);
    ctx.beginPath();
    ctx.fillStyle = caminho.includes(l.nome) ? "#007acc" : "#555";
    ctx.shadowColor = "rgba(0,0,0,0.4)";
    ctx.shadowBlur = 4;
    ctx.arc(x, y, 8, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    ctx.shadowBlur = 0;
  });

  if (animando) {
    const p = animarBola(proj);
    if (p) {
      ctx.beginPath();
      ctx.fillStyle = "#ff5722";
      ctx.shadowColor = "#ff5722";
      ctx.shadowBlur = 15;
      ctx.arc(...p, 10, 0, 2 * Math.PI);
      ctx.fill();
      ctx.shadowBlur = 0;
    }
  }
}

function animarBola(proj) {
  if (bolaIdx >= caminho.length - 1) return null;
  const i = Math.floor(bolaIdx);
  const f = bolaIdx - i;
  const a = proj(...pos[caminho[i]]);
  const b = proj(...pos[caminho[i + 1]]);
  return [a[0] + f * (b[0] - a[0]), a[1] + f * (b[1] - a[1])];
}

function iniciarAnim() {
  bolaIdx = 0;
  animando = true;
  if (animId) cancelAnimationFrame(animId);
  function step() {
    desenhar();
    bolaIdx += 0.02;
    if (evento && evento.tipo === "bloqueio" && caminho.length > 1) {
      for (let i = 0; i < caminho.length - 1; i++) {
        const a = [caminho[i], caminho[i + 1]];
        if (
          (a[0] === evento.aresta[0] && a[1] === evento.aresta[1]) ||
          (a[0] === evento.aresta[1] && a[1] === evento.aresta[0])
        ) {
          calcularRota();
          return;
        }
      }
    }
    if (bolaIdx < caminho.length - 1) animId = requestAnimationFrame(step);
    else {
      animando = false;
      desenhar();
    }
  }
  step();
}

function atualizarDetalhesRota(caminho, custo, tempo) {
  detalhesEl.innerHTML = "";
  if (caminho.length < 2) {
    detalhesEl.textContent = "Nenhuma rota calculada.";
    return;
  }

  caminho.forEach((n, i) => {
    const li = document.createElement("li");
    li.textContent =
      i === caminho.length - 1
        ? `Destino final: ${n}`
        : `Passar por: ${n} ➡️ Próximo: ${caminho[i + 1]}`;
    detalhesEl.appendChild(li);
  });

  const liCusto = document.createElement("li");
  liCusto.textContent = `Distância total: ${custo.toFixed(2)} km`;
  detalhesEl.appendChild(liCusto);

  const liTempo = document.createElement("li");
  liTempo.textContent = `Tempo estimado: ${tempo.toFixed(2)} min`;
  detalhesEl.appendChild(liTempo);
}

async function calcularRota() {
  if (origemSelect.value === destinoSelect.value) {
    statusEl.textContent = "Origem e destino não podem ser iguais.";
    return;
  }
  statusEl.textContent = "Calculando...";
  eventoEl.textContent = custoEl.textContent = "";
  detalhesEl.textContent = "";

  const payload = {
    origem: origemSelect.value,
    destino: destinoSelect.value,
  };

  try {
    const res = await fetch("/api/rota", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok || !data.caminho || data.caminho.length === 0) {
      statusEl.textContent = "Erro ao calcular rota.";
      caminho = [];
      custo = 0;
      tempoEstimado = 0;
    } else {
      caminho = data.caminho;
      custo = data.custo;
      tempoEstimado = data.custo * 2; // Suponha 30 km/h = 2 min/km
      statusEl.textContent = "Rota calculada com sucesso!";
      custoEl.textContent = `Distância: ${custo.toFixed(2)} km`;
      atualizarDetalhesRota(caminho, custo, tempoEstimado);
      iniciarAnim();
    }
  } catch (err) {
    statusEl.textContent = "Erro na comunicação com o servidor.";
    caminho = [];
    custo = 0;
  }

  desenhar();
}

function gerarEvento() {
  if (Math.random() < 0.3 && locais.length > 1) {
    const orig = locais[Math.floor(Math.random() * locais.length)].nome;
    const destinos = grafoSimples[orig];
    if (!destinos || destinos.length === 0) return null;
    const dest = destinos[Math.floor(Math.random() * destinos.length)];
    const tipo = Math.random() < 0.5 ? "bloqueio" : "congestionamento";
    return {
      tipo,
      aresta: [orig, dest],
      descricao:
        tipo === "bloqueio"
          ? `Bloqueio na rota entre ${orig} e ${dest}`
          : `Congestionamento entre ${orig} e ${dest}, tráfego lento`,
    };
  }
  return null;
}

function atualizarEvento() {
  evento = gerarEvento();
  if (!evento) {
    eventoEl.textContent = "Nenhum evento na rota.";
    desenhar();
    return;
  }
  eventoEl.textContent = `Evento: ${evento.descricao}`;
  if (evento.tipo === "bloqueio") {
    grafoSimples[evento.aresta[0]] = grafoSimples[evento.aresta[0]].filter(
      v => v !== evento.aresta[1]
    );
    grafoSimples[evento.aresta[1]] = grafoSimples[evento.aresta[1]].filter(
      v => v !== evento.aresta[0]
    );
  }
  desenhar();
}

function alternarTema() {
  const isDark = document.documentElement.getAttribute("data-theme") === "dark";
  if (isDark) {
    document.documentElement.setAttribute("data-theme", "light");
    document.body.classList.remove("dark-mode");
    toggleBtn.textContent = "Modo Escuro";
  } else {
    document.documentElement.setAttribute("data-theme", "dark");
    document.body.classList.add("dark-mode");
    toggleBtn.textContent = "Modo Claro";
  }
}

btn.addEventListener("click", calcularRota);
toggleBtn.addEventListener("click", alternarTema);

(async () => {
  ajustarCanvas();
  await carregarLocais();
  construirGrafo();
  desenhar();
  atualizarEvento();
  setInterval(() => {
    construirGrafo();
    atualizarEvento();
  }, 20000);
})();

window.addEventListener("resize", () => {
  ajustarCanvas();
  desenhar();
});
