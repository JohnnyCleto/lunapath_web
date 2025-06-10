import networkx as nx

# 50 locais com coordenadas fixas (estilo cidade inteligente)
LOCAIS = {
    "Casa de Luna": (0, 0),
    "Estação de Drones": (2, 1),
    "Auditoria Principal": (4, 0),
    "Estação IoT": (1, 3),
    "Cafeteria Tech": (3, 2),
    "Central de Energia": (5, 1),
    "Hospital Futuro": (6, 3),
    "Escola Smart": (2, 4),
    "Museu Digital": (3, 5),
    "Estúdio Holográfico": (5, 5),
    "Praça do Conhecimento": (0, 5),
    "Biblioteca AR": (1, 6),
    "Centro de Robótica": (4, 6),
    "Galeria Virtual": (6, 6),
    "Laboratório Quântico": (7, 2),
    "Centro de Inovação": (7, 4),
    "Mercado Automatizado": (3, 7),
    "Estação Solar": (6, 0),
    "Zoológico Digital": (8, 3),
    "Residência Cyborg": (7, 6),
    "Teatro de Realidade Mista": (8, 5),
    "Parque Inteligente": (0, 2),
    "Clínica de Nanomedicina": (5, 3),
    "Delegacia Neural": (1, 1),
    "Terminal de Ônibus Autônomo": (4, 4),
    "Garagem de Veículos AI": (2, 2),
    "Torre de Comunicação 5G": (0, 6),
    "Observatório de Dados": (6, 7),
    "Laboratório Genético": (3, 1),
    "Academia VR": (8, 1),
    "Centro Financeiro Blockchain": (1, 5),
    "Cinema Imersivo": (7, 1),
    "Ponto de Recarga Elétrica": (2, 6),
    "Estufa Inteligente": (4, 7),
    "Fábrica Automatizada": (5, 6),
    "Base de Drones": (3, 3),
    "Túnel Subterrâneo A": (6, 2),
    "Túnel Subterrâneo B": (0, 3),
    "Ponto de Encontro AR": (2, 0),
    "Posto de Vigilância": (7, 3),
    "Jardim Algorítmico": (6, 5),
    "Escola Infantil Digital": (1, 4),
    "Restaurante Autônomo": (2, 5),
    "Campus AI": (7, 7),
    "Condomínio Verde": (5, 7),
    "Vila Modular": (4, 2),
    "Câmara de Simulação": (3, 4),
    "Núcleo de Energia Limpa": (8, 0),
    "Rooftop Garden": (6, 1),
    "Estação Suborbital": (9, 2),
    "Trilha Sensorial": (8, 6),
}

# Lista de conexões entre os locais com pesos (tempo estimado)
CONEXOES = [
    ("Casa de Luna", "Estação de Drones", 4),
    ("Casa de Luna", "Parque Inteligente", 3),
    ("Casa de Luna", "Delegacia Neural", 5),
    ("Estação de Drones", "Auditoria Principal", 3),
    ("Estação de Drones", "Cafeteria Tech", 2),
    ("Estação IoT", "Casa de Luna", 6),
    ("Estação IoT", "Escola Smart", 3),
    ("Cafeteria Tech", "Base de Drones", 2),
    ("Base de Drones", "Clínica de Nanomedicina", 2),
    ("Clínica de Nanomedicina", "Hospital Futuro", 3),
    ("Hospital Futuro", "Posto de Vigilância", 2),
    ("Posto de Vigilância", "Centro de Inovação", 1),
    ("Centro de Inovação", "Residência Cyborg", 2),
    ("Residência Cyborg", "Teatro de Realidade Mista", 2),
    ("Teatro de Realidade Mista", "Trilha Sensorial", 1),
    ("Trilha Sensorial", "Campus AI", 1),
    ("Campus AI", "Observatório de Dados", 2),
    ("Observatório de Dados", "Estufa Inteligente", 2),
    ("Estufa Inteligente", "Fábrica Automatizada", 1),
    ("Fábrica Automatizada", "Centro de Robótica", 2),
    ("Centro de Robótica", "Museu Digital", 2),
    ("Museu Digital", "Centro Financeiro Blockchain", 2),
    ("Centro Financeiro Blockchain", "Escola Infantil Digital", 1),
    ("Escola Infantil Digital", "Escola Smart", 1),
    ("Escola Smart", "Garagem de Veículos AI", 2),
    ("Garagem de Veículos AI", "Laboratório Genético", 1),
    ("Laboratório Genético", "Auditoria Principal", 2),
    ("Laboratório Genético", "Cafeteria Tech", 1),
    ("Cafeteria Tech", "Vila Modular", 1),
    ("Vila Modular", "Clínica de Nanomedicina", 2),
    ("Auditoria Principal", "Estação Solar", 2),
    ("Estação Solar", "Núcleo de Energia Limpa", 2),
    ("Núcleo de Energia Limpa", "Academia VR", 2),
    ("Academia VR", "Estação Suborbital", 2),
    ("Estação Suborbital", "Zoológico Digital", 1),
    ("Zoológico Digital", "Posto de Vigilância", 1),
    ("Museu Digital", "Praça do Conhecimento", 2),
    ("Praça do Conhecimento", "Biblioteca AR", 1),
    ("Biblioteca AR", "Torre de Comunicação 5G", 1),
    ("Torre de Comunicação 5G", "Centro Financeiro Blockchain", 1),
    ("Garagem de Veículos AI", "Ponto de Encontro AR", 2),
    ("Delegacia Neural", "Ponto de Encontro AR", 1),
    ("Túnel Subterrâneo A", "Hospital Futuro", 1),
    ("Túnel Subterrâneo A", "Laboratório Quântico", 2),
    ("Laboratório Quântico", "Cinema Imersivo", 1),
    ("Cinema Imersivo", "Academia VR", 2),
    ("Túnel Subterrâneo B", "Estação IoT", 2),
    ("Túnel Subterrâneo B", "Praça do Conhecimento", 1),
    ("Rooftop Garden", "Clínica de Nanomedicina", 2),
]

def gerar_mapa_cidade():
    cidade = nx.Graph()
    for nome, (x, y) in LOCAIS.items():
        cidade.add_node(nome, pos=(x, y))
    for origem, destino, peso in CONEXOES:
        cidade.add_edge(origem, destino, weight=peso)
    return cidade

def dijkstra(grafo, origem):
    dist = {node: float('inf') for node in grafo.nodes}
    dist[origem] = 0
    ant = {node: None for node in grafo.nodes}
    visitados = set()

    while len(visitados) < len(grafo.nodes):
        atual = min((n for n in grafo.nodes if n not in visitados), key=lambda n: dist[n])
        visitados.add(atual)

        for vizinho in grafo.neighbors(atual):
            peso = grafo[atual][vizinho]["weight"]
            if dist[atual] + peso < dist[vizinho]:
                dist[vizinho] = dist[atual] + peso
                ant[vizinho] = atual

    return dist, ant

def reconstruir_rota(anteriores, origem, destino):
    rota = []
    atual = destino
    while atual != origem:
        anterior = anteriores[atual]
        if anterior is None:
            return []
        rota.append((anterior, atual))
        atual = anterior
    rota.reverse()
    return rota
