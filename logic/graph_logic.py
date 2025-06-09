import networkx as nx
import random

def gerar_mapa_inteligente(total_pontos):
    G = nx.Graph()
    locais = [f"Local {i+1}" for i in range(total_pontos)]

    for local in locais:
        G.add_node(local)

    for i in range(total_pontos):
        for j in range(i + 1, total_pontos):
            if random.random() < 0.6:
                tempo = random.randint(2, 15)
                G.add_edge(locais[i], locais[j], weight=tempo)

    return G, locais

def dijkstra(grafo, inicio):
    dist = {n: float("inf") for n in grafo.nodes}
    ant = {}
    dist[inicio] = 0
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        atual = min((n for n in grafo.nodes if n not in visitados), key=lambda n: dist[n], default=None)
        if atual is None:
            break
        for viz in grafo.neighbors(atual):
            peso = grafo[atual][viz]["weight"]
            nova_dist = dist[atual] + peso
            if nova_dist < dist[viz]:
                dist[viz] = nova_dist
                ant[viz] = atual
        visitados.add(atual)

    return dist, ant

def reconstruir_rota(anteriores, inicio, destino):
    rota = []
    atual = destino
    while atual != inicio:
        anterior = anteriores.get(atual)
        if anterior is None:
            return []
        rota.append((anterior, atual))
        atual = anterior
    return rota[::-1]
