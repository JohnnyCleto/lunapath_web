from flask import Flask, request, jsonify, render_template
from logic.graph_logic import gerar_mapa_cidade, dijkstra_dinamico, reconstruir_rota, atualizar_pesos_iot
import threading
import time
import random
import copy

app = Flask(__name__)

grafo_original = gerar_mapa_cidade()
grafo_global = copy.deepcopy(grafo_original)

# Inicializando sensores IoT para ambas as direções
sensores_iot = {}
for u, v in grafo_global.edges():
    sensores_iot[(u, v)] = random.uniform(0, 0.6)
    sensores_iot[(v, u)] = sensores_iot[(u, v)]  # sempre bidirecional

lock = threading.Lock()

def atualizar_grafo_periodicamente():
    while True:
        with lock:
            for edge in list(sensores_iot.keys()):
                novo_valor = random.uniform(0, 1)
                sensores_iot[edge] = novo_valor
                sensores_iot[(edge[1], edge[0])] = novo_valor  # mantém simetria
            atualizar_pesos_iot(grafo_global, sensores_iot)
        time.sleep(5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/mapa")
def mapa():
    with lock:
        nodes = [{
            "id": node,
            "label": node,
            "x": grafo_global.nodes[node]["pos"][0],
            "y": grafo_global.nodes[node]["pos"][1]
        } for node in grafo_global.nodes]

        edges = []
        for u, v, d in grafo_global.edges(data=True):
            congestion = round(sensores_iot.get((u, v), 0), 2)
            edges.append({
                "from": u,
                "to": v,
                "weight": round(d["weight"], 2),
                "congestion": congestion,
            })

    return jsonify({"nodes": nodes, "edges": edges})

@app.route("/api/rota", methods=["POST"])
def rota():
    data = request.json
    origem = data.get("origem")
    destino = data.get("destino")
    prioridade = data.get("prioridade", "tempo")

    if origem not in grafo_global or destino not in grafo_global:
        return jsonify({"erro": "Origem ou destino inválido."}), 400

    with lock:
        # Backup completo
        backup_grafo = copy.deepcopy(grafo_global)
        backup_sensores = copy.deepcopy(sensores_iot)

        dist, ant = dijkstra_dinamico(grafo_global, origem, prioridade)
        rota_inicial = reconstruir_rota(ant, origem, destino)
        tempo_inicial = dist.get(destino, float("inf"))

        if not rota_inicial or tempo_inicial == float("inf"):
            return jsonify({"erro": "Não foi possível calcular a rota inicial."}), 400

        evento = random.choices(
            ["normal", "bloqueio", "desvio", "congestionamento_extremo"],
            weights=[0.7, 0.1, 0.15, 0.05],
            k=1,
        )[0]

        rota_final = rota_inicial
        tempo_final = tempo_inicial
        descricao_evento = "Rota calculada normalmente sem imprevistos."

        try:
            if evento == "bloqueio" and len(rota_inicial) > 2:
                u, v = rota_inicial[1], rota_inicial[2]
                if grafo_global.has_edge(u, v):
                    grafo_global.remove_edge(u, v)
                    dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, prioridade)
                    nova_rota = reconstruir_rota(ant_alt, origem, destino)
                    tempo_alt = dist_alt.get(destino, float("inf"))
                    if nova_rota and tempo_alt != float("inf"):
                        rota_final = nova_rota
                        tempo_final = tempo_alt
                        descricao_evento = f"Bloqueio na via entre '{u}' e '{v}'. Rota alternativa calculada."
                    else:
                        descricao_evento = f"Bloqueio entre '{u}' e '{v}', mas nenhuma rota alternativa encontrada."

            elif evento == "desvio":
                fator = random.uniform(1.2, 1.4)
                for u, v in grafo_global.edges():
                    grafo_global[u][v]["weight"] *= fator
                dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, prioridade)
                nova_rota = reconstruir_rota(ant_alt, origem, destino)
                tempo_alt = dist_alt.get(destino, float("inf"))
                if nova_rota and tempo_alt != float("inf"):
                    rota_final = nova_rota
                    tempo_final = tempo_alt
                    descricao_evento = "Desvio na rota causado por aumento nos tempos das vias."

            elif evento == "congestionamento_extremo":
                for edge in list(sensores_iot.keys()):
                    novo_valor = random.uniform(0.7, 1.0)
                    sensores_iot[edge] = novo_valor
                    sensores_iot[(edge[1], edge[0])] = novo_valor
                atualizar_pesos_iot(grafo_global, sensores_iot)
                dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, "evitar_congestionamento")
                nova_rota = reconstruir_rota(ant_alt, origem, destino)
                tempo_alt = dist_alt.get(destino, float("inf"))
                if nova_rota and tempo_alt != float("inf"):
                    rota_final = nova_rota
                    tempo_final = tempo_alt
                    descricao_evento = "Congestionamento extremo detectado. Rota otimizada."

        finally:
            # Sempre restaura grafo e sensores depois da simulação
            grafo_global.clear()
            grafo_global.add_nodes_from(backup_grafo.nodes(data=True))
            grafo_global.add_edges_from(backup_grafo.edges(data=True))
            sensores_iot.clear()
            sensores_iot.update(backup_sensores)

        if not rota_final or tempo_final == float("inf"):
            return jsonify({"erro": "Falha ao encontrar rota alternativa."}), 400

    return jsonify({
        "rota": rota_final,
        "tempo_total": round(tempo_final, 2),
        "evento": evento,
        "descricao_evento": descricao_evento,
        "total_pontos": len(rota_final)
    })

if __name__ == "__main__":
    thread = threading.Thread(target=atualizar_grafo_periodicamente, daemon=True)
    thread.start()
    app.run(debug=True)
