from flask import Flask, request, jsonify, render_template
from logic.graph_logic import (
    gerar_mapa_cidade,
    dijkstra_dinamico,
    reconstruir_rota,
    atualizar_pesos_iot,
)
import threading
import time
import random
import copy

app = Flask(__name__)

# Grafo base e cópia para manipulação
grafo_original = gerar_mapa_cidade()
grafo_global = copy.deepcopy(grafo_original)

# Sensores IoT simulando congestionamento inicial (0 a 0.6)
sensores_iot = {edge: random.uniform(0, 0.6) for edge in grafo_global.edges()}

lock = threading.Lock()

def atualizar_grafo_periodicamente():
    """
    Atualiza os pesos do grafo baseando-se no congestionamento dos sensores IoT.
    Executa em thread separada.
    """
    while True:
        with lock:
            for edge in sensores_iot:
                sensores_iot[edge] = random.uniform(0, 1)
            atualizar_pesos_iot(grafo_global, sensores_iot)
        time.sleep(5)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/mapa")
def mapa():
    """
    Retorna dados dos nós e arestas para visualização.
    """
    with lock:
        nodes = [
            {
                "id": node,
                "label": node,
                "x": grafo_global.nodes[node]["pos"][0],
                "y": grafo_global.nodes[node]["pos"][1],
            }
            for node in grafo_global.nodes
        ]

        edges = []
        for u, v, d in grafo_global.edges(data=True):
            congestion = round(sensores_iot.get((u, v), sensores_iot.get((v, u), 0)), 2)
            edges.append({
                "from": u,
                "to": v,
                "weight": round(d["weight"], 2),
                "congestion": congestion,
            })

    return jsonify({"nodes": nodes, "edges": edges})

@app.route("/api/rota", methods=["POST"])
def rota():
    """
    Calcula rota inicial e, só depois, simula eventos imprevistos que podem alterar a rota.
    Retorna rota final, tempo e evento ocorrido.
    """
    data = request.json
    origem = data.get("origem")
    destino = data.get("destino")
    prioridade = data.get("prioridade", "tempo")  # 'tempo' ou 'evitar_congestionamento'

    if origem not in grafo_global or destino not in grafo_global:
        return jsonify({"erro": "Origem ou destino inválido."}), 400

    with lock:
        # Backup para restaurar após simulação
        backup_grafo = copy.deepcopy(grafo_global)
        backup_sensores = sensores_iot.copy()

        # Cálculo inicial da rota
        dist, ant = dijkstra_dinamico(grafo_global, origem, prioridade)
        rota_inicial = reconstruir_rota(ant, origem, destino)
        tempo_inicial = dist.get(destino, float("inf"))

        if not rota_inicial or tempo_inicial == float("inf"):
            return jsonify({"erro": "Não foi possível calcular a rota inicial."}), 400

        # Simula evento após cálculo inicial
        evento = random.choices(
            ["normal", "bloqueio", "desvio", "congestionamento_extremo"],
            weights=[0.7, 0.1, 0.15, 0.05],
            k=1,
        )[0]

        rota_final = rota_inicial
        tempo_final = tempo_inicial

        if evento != "normal":
            if evento == "bloqueio":
                # Remove aresta próxima ao início para simular bloqueio
                if len(rota_inicial) > 2:
                    u, v = rota_inicial[1], rota_inicial[2]
                    if grafo_global.has_edge(u, v):
                        grafo_global.remove_edge(u, v)
                        dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, prioridade)
                        nova_rota = reconstruir_rota(ant_alt, origem, destino)
                        tempo_alt = dist_alt.get(destino, float("inf"))
                        if nova_rota and tempo_alt != float("inf"):
                            rota_final = nova_rota
                            tempo_final = tempo_alt

            elif evento == "desvio":
                # Aumenta pesos das arestas para simular desvio (rotas mais longas)
                for u, v in grafo_global.edges():
                    fator = random.uniform(1.1, 1.5)
                    grafo_global[u][v]["weight"] *= fator
                dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, prioridade)
                nova_rota = reconstruir_rota(ant_alt, origem, destino)
                tempo_alt = dist_alt.get(destino, float("inf"))
                if nova_rota and tempo_alt != float("inf"):
                    rota_final = nova_rota
                    tempo_final = tempo_alt

            elif evento == "congestionamento_extremo":
                # Ajusta sensores para congestionamento extremo
                for edge in sensores_iot:
                    sensores_iot[edge] = random.uniform(0.7, 1.0)
                atualizar_pesos_iot(grafo_global, sensores_iot)
                dist_alt, ant_alt = dijkstra_dinamico(grafo_global, origem, "evitar_congestionamento")
                nova_rota = reconstruir_rota(ant_alt, origem, destino)
                tempo_alt = dist_alt.get(destino, float("inf"))
                if nova_rota and tempo_alt != float("inf"):
                    rota_final = nova_rota
                    tempo_final = tempo_alt

        # Restaura grafo e sensores ao estado original
        grafo_global.clear()
        grafo_global.add_nodes_from(backup_grafo.nodes(data=True))
        grafo_global.add_edges_from(backup_grafo.edges(data=True))
        sensores_iot.update(backup_sensores)

        if not rota_final or tempo_final == float("inf"):
            return jsonify({"erro": "Falha ao encontrar rota alternativa."}), 400

    return jsonify({
        "rota": rota_final,
        "tempo_total": round(tempo_final, 2),
        "evento": evento
    })

if __name__ == "__main__":
    thread = threading.Thread(target=atualizar_grafo_periodicamente, daemon=True)
    thread.start()
    app.run(debug=True)
