from flask import Flask, render_template, jsonify, request
from logic import graph_logic
import random

app = Flask(__name__, static_folder="static", template_folder="templates")
G = graph_logic.criar_grafo()
evento_atual = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/locais")
def api_locais():
    dados = []
    for nome, (x, y, tipo) in graph_logic.LOCAIS.items():
        dados.append([nome, {"pos": (x, y), "tipo": tipo}])
    return jsonify(dados)

@app.route("/api/rota", methods=["POST"])
def api_rota():
    global evento_atual
    dados = request.get_json(silent=True)
    if not dados or "origem" not in dados or "destino" not in dados:
        return jsonify({"erro": "JSON inválido."}), 400
    origem = dados["origem"]
    destino = dados["destino"]
    if origem not in G.nodes or destino not in G.nodes:
        return jsonify({"erro": "Origem ou destino inválido."}), 400

    G_temp = G.copy()
    if evento_atual and evento_atual.get("tipo") == "bloqueio":
        edge = evento_atual.get("aresta")
        if edge and G_temp.has_edge(*edge):
            G_temp.remove_edge(*edge)

    try:
        caminho, _ = graph_logic.dijkstra(G_temp, origem, destino)
        custo = graph_logic.calcular_custo_caminho(G_temp, caminho)
    except:
        return jsonify({"erro": "Falha ao calcular rota."}), 500

    evento_atual = None
    if random.random() < 0.25:
        tipo = random.choice(["bloqueio", "atraso", "desvio"])
        if tipo == "bloqueio" and len(caminho) > 1:
            idx = random.randrange(len(caminho) - 1)
            aresta = (caminho[idx], caminho[idx + 1])
            evento_atual = {"tipo": "bloqueio", "aresta": aresta, "descricao": f"Bloqueio entre {aresta[0]} e {aresta[1]}"}
        elif tipo == "atraso":
            inc = random.uniform(0.1, 0.3)
            custo *= 1 + inc
            evento_atual = {"tipo": "atraso", "descricao": f"Atraso ~{int(inc*100)}% no tempo estimado"}
        elif tipo == "desvio" and len(G_temp.edges) > 0:
            e = random.choice(list(G_temp.edges))
            G_temp.remove_edge(*e)
            try:
                caminho2, _ = graph_logic.dijkstra(G_temp, origem, destino)
                caminho = caminho2
                custo = graph_logic.calcular_custo_caminho(G_temp, caminho)
                evento_atual = {"tipo": "desvio", "aresta": e, "descricao": f"Desvio por problema entre {e[0]} e {e[1]}"}
            except:
                evento_atual = None

    return jsonify({"caminho": caminho, "custo": round(custo, 2), "evento": evento_atual})

@app.route("/api/evento")
def api_evento():
    return jsonify(evento_atual or {})

if __name__ == "__main__":
    app.run(debug=True)
