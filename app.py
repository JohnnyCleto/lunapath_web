from flask import Flask, request, jsonify, render_template
from logic.graph_logic import gerar_mapa_inteligente, dijkstra, reconstruir_rota

app = Flask(__name__)
grafo_global = None
locais_global = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/mapa", methods=["POST"])
def gerar_mapa():
    global grafo_global, locais_global
    data = request.json
    total = data.get("pontos")
    grafo_global, locais_global = gerar_mapa_inteligente(total)
    return jsonify({
        "locais": locais_global,
        "arestas": [
            {"from": u, "to": v, "weight": d["weight"]}
            for u, v, d in grafo_global.edges(data=True)
        ]
    })

@app.route("/api/rota", methods=["POST"])
def calcular_rota():
    data = request.json
    origem = data.get("origem")
    destino = data.get("destino")

    if origem not in grafo_global or destino not in grafo_global:
        return jsonify({"erro": "Ponto inválido"}), 400

    dist, ant = dijkstra(grafo_global, origem)
    rota = reconstruir_rota(ant, origem, destino)
    return jsonify({
        "rota": rota,
        "tempo_total": dist[destino]
    })

if __name__ == "__main__":
    app.run(debug=True)
