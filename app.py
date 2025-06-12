from flask import Flask, render_template, request, jsonify
from logic.graph_logic import simular_rota, gerar_grafo, obter_posicoes
import json

app = Flask(__name__)

grafo_global = gerar_grafo()  # Mantém grafo estático para frontend

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/locais")
def api_locais():
    # Retorna lista de locais para dropdown no frontend
    locais = list(grafo_global.nodes)
    return jsonify(locais)

@app.route("/api/rota", methods=["POST"])
def api_rota():
    data = request.json
    origem = data.get("origem")
    destino = data.get("destino")
    if origem not in grafo_global.nodes or destino not in grafo_global.nodes:
        return jsonify({"error": "Origem ou destino inválidos"}), 400

    # Chama simulação de rota
    caminho, custo, rota_alternativa = simular_rota(origem, destino)
    # Prepara resposta para frontend
    resp = {
        "caminho": caminho,
        "custo": round(custo, 2),
        "rota_alternativa": rota_alternativa,
        "posicoes": obter_posicoes(grafo_global),
        "arestas": [
            {"u": u, "v": v,
             "peso": grafo_global[u][v]['weight'],
             "congestion": grafo_global[u][v].get('congestion', 1),
             "blocked": grafo_global[u][v].get('blocked', False)
            }
            for u, v in grafo_global.edges
        ]
    }
    return jsonify(resp)

if __name__ == "__main__":
    app.run(debug=True)
