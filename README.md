# lunapath_web

---

# 🗺️ Um Mapa, Muitos Caminhos: A História do Nosso Projeto de Rotas

Tudo começou com uma pergunta simples:
**"E se pudéssemos mostrar o caminho mais rápido entre dois pontos... e se ele mudasse no meio do trajeto?"**

Foi assim que nasceu este projeto — não como um produto pronto, mas como uma ideia viva, curiosa e dinâmica. Queríamos mais do que apenas desenhar linhas num mapa. Queríamos **simular o imprevisível**, como o bloqueio de uma rua ou um congestionamento inesperado. E, principalmente, queríamos que qualquer pessoa pudesse ver isso acontecer **em tempo real**, direto na tela.

---

## 🎨 O Que Você Vai Ver

Ao abrir a aplicação, você se depara com um mapa interativo. Ele não é um mapa de verdade — mas representa lugares conectados como pontos em uma rede. Esses pontos são conectados por linhas, e você pode escolher um ponto de origem e um destino.

Quando clica em "Calcular Rota", algo mágico acontece:
🚗 Uma bolinha começa a se mover, animada, percorrendo o trajeto mais curto.

Mas o caminho não é garantido. A cada poucos segundos, algo pode acontecer:

* 🚧 Um bloqueio força a bolinha a recalcular a rota.
* 🐢 Um atraso aumenta o tempo de viagem.
* 🔄 Um desvio muda completamente o percurso.

Esses eventos surgem aleatoriamente, porque é assim que a vida funciona — cheia de surpresas.

---

## 🧠 Por Trás das Cenas

Por trás desse mapa dançante estão três mentes:

* O **código JavaScript** (`map.js`) que desenha, anima e atualiza tudo que acontece na tela.
* O **servidor Flask** (`app.py`) que calcula rotas, lida com eventos aleatórios e responde às requisições.
* E a **lógica de grafos** (escondida no `graph_logic.py`), que conhece todos os caminhos possíveis — e sabe qual é o melhor.

Juntos, eles formam o cérebro e o coração dessa aplicação: um sistema que simula uma pequena cidade virtual e seus imprevistos.

---

## ✨ Por Que Isso Importa?

Porque entender caminhos não é só sobre algoritmos.
É sobre **navegar no inesperado**.

Este projeto foi feito para mostrar que mesmo com lógica, planejamento e direções claras, o mundo muda. Mas sempre há outra rota — e às vezes, a reviravolta nos leva a um caminho melhor.

---

## 📌 Para Desenvolvedores Curiosos

Se você quiser mergulhar no código, ver como cada parte se comunica, ou até adaptar o mapa para sua cidade, está tudo pronto para você.

Mas mesmo que você não toque uma linha, queremos que ao menos você sinta o que sentimos ao construir isso:
🧭 A beleza de um caminho traçado — e o fascínio do que pode acontecer no meio do percurso.

---

Seja bem-vindo à jornada.
Escolha seu ponto de partida, e prepare-se: o caminho pode mudar — mas sempre valerá a pena.

---

