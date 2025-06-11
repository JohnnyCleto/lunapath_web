from flask import Flask, request, jsonify, render_template
from logic.graph_logic import gerar_mapa_cidade, dijkstra, reconstruir_rota

app = Flask(__name__)
grafo_global = gerar_mapa_cidade()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/mapa")
def mapa():
    # Retorna os nós e arestas com posições x, y e peso
    return jsonify({
        "nodes": [
            {"id": node, "label": node, "x": grafo_global.nodes[node]["pos"][0], "y": grafo_global.nodes[node]["pos"][1]}
            for node in grafo_global.nodes
        ],
        "edges": [
            {"from": u, "to": v, "weight": d["weight"]}
            for u, v, d in grafo_global.edges(data=True)
        ]
    })

@app.route("/api/rota", methods=["POST"])
def rota():
    data = request.json
    origem = data.get("origem")
    destino = data.get("destino")

    if origem not in grafo_global or destino not in grafo_global:
        return jsonify({"erro": "Ponto inválido"}), 400

    dist, ant = dijkstra(grafo_global, origem)
    rota = reconstruir_rota(ant, origem, destino)
    return jsonify({"rota": rota, "tempo_total": dist[destino]})

if __name__ == "__main__":
    app.run(debug=True)
