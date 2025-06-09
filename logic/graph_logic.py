import networkx as nx
import random

def gerar_mapa_inteligente(total_pontos):
    municipio = nx.Graph()
    locais = [f"Local {i+1}" for i in range(total_pontos)]
    
    for local in locais:
        municipio.add_node(local)

    for i in range(total_pontos):
        for j in range(i+1, total_pontos):
            if random.random() < 0.5:
                tempo = random.randint(1, 20)
                municipio.add_edge(locais[i], locais[j], weight=tempo)

    return municipio

def dijkstra(mapa, inicio):
    distancias = {no: float('inf') for no in mapa.nodes}
    anteriores = {}
    distancias[inicio] = 0
    visitados = set()

    while len(visitados) < len(mapa.nodes):
        atual = min((n for n in mapa.nodes if n not in visitados),
                    key=lambda n: distancias[n], default=None)
        if atual is None:
            break
        for vizinho in mapa.neighbors(atual):
            peso = mapa[atual][vizinho]['weight']
            nova_distancia = distancias[atual] + peso
            if nova_distancia < distancias[vizinho]:
                distancias[vizinho] = nova_distancia
                anteriores[vizinho] = atual
        visitados.add(atual)
    return distancias, anteriores

def reconstruir_rota(anteriores, inicio, destino):
    rota = []
    atual = destino
    while atual != inicio:
        anterior = anteriores.get(atual)
        if anterior is None:
            return []
        rota.append((anterior, atual))
        atual = anterior
    return list(reversed(rota))
