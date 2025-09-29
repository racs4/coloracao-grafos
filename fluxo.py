import sys
import heapq


class AdjNode:
    def __init__(self, vertex: int, capacity: int, flow: int, type: int, twin=None):
        self.vertex = vertex
        self.capacity = capacity
        self.flow = flow
        self.type = type
        self.twin = twin


class Graph:
    def __init__(self, V: int, A: int):
        self.V = V
        self.A = A
        # List of lists to hold adjacency nodes
        self.adj = [[] for _ in range(V)]

    def add_edge(self, u: int, v: int, capacity: int):
        forward = AdjNode(v, capacity, 0, 1, None)
        self.adj[u].append(forward)

    def reset_flows(self):
        for i in range(self.V):
            for node in self.adj[i]:
                node.flow = 0
                node.twin = None

    def print_flows(self, show_empty=False):
        for i in range(self.V):
            for node in self.adj[i]:
                if node.flow > 0 or show_empty:
                    print(
                        f"{i} -> {node.vertex} : {node.flow}/{node.capacity}")

    def print_adj(self):
        print("Graph adjacency list:")
        for i in range(self.V):
            for node in self.adj[i]:
                print(
                    f"{i} -> {node.vertex} : {node.flow}/{node.capacity} (type={node.type})")

    def expand(self):
        for i in range(self.V):
            for node in self.adj[i]:
                if node.twin is None:
                    twin = AdjNode(i, 0, 0, -1, node)
                    node.twin = twin
                    self.adj[node.vertex].append(twin)

    def contract(self):
        for i in range(self.V):
            self.adj[i] = [node for node in self.adj[i] if node.type == 1]

    def get_max_flow(self, source: int, sink: int, augmenting_path) -> int:
        self.reset_flows()
        self.expand()
        intensity = 0
        while True:
            delta, parents = augmenting_path(self, source, sink)
            if delta == -1:
                break
            v = sink
            print(f"Augmenting path found with flow {delta}: ", end="")
            while v != source:
                print(v, end=" <- ")
                u, node = parents[v]
                if node is None:
                    continue
                node.flow += delta
                node.twin.flow -= delta
                v = u
            print(source)
            print("Graph state after finding path:")
            self.print_flows()
            intensity += delta
        # print("Final flow state:")
        # self.print_flows()
        self.contract()
        return intensity


def dfs_augmenting_path(graph: Graph, source: int, sink: int) -> tuple[int, list[tuple[int, None]]]:
    '''
    Modo genérico de busca de caminho aumentante.
    Faz um dfs normal, mas também olha a capacidade residual (capacity - flow) de cada aresta.
    Tem complexidade O(V + A) de um dfs normal.
    Garantido que será chamada menos que VM vezes, onde M é a capacidade máxima do grafo.
    Intuição da prova:
    - Cada vez que o algoritmo executa ele diminui pelo menos 1 unidade da capacidade de alguma aresta.
    - O número máximo de arcos que saem da fonte é menor que V.
    - Portanto, o número máximo de caminhos aumentantes é VM.
    '''
    visited = [False] * graph.V
    parent = [(-1, None)] * graph.V

    pilha = [source]
    visited[source] = True
    while pilha:
        u = pilha.pop()
        for node in graph.adj[u]:
            v = node.vertex
            if not visited[v] and node.capacity - node.flow > 0:
                visited[v] = True
                parent[v] = (u, node)
                if v == sink:
                    break
                pilha.append(v)
        if visited[sink]:
            break

    if not visited[sink]:
        return -1, parent

    # Find the maximum flow through the path found.
    delta = sys.maxsize
    v = sink
    while v != source:
        u, node = parent[v]
        if node is None:
            continue
        delta = min(delta, node.capacity - node.flow)
        v = u

    return delta, parent


def bfs_augmenting_path(graph: Graph, source: int, sink: int) -> tuple[int, list[tuple[int, None]]]:
    '''
    Busca pelo menor caminho aumentante (em termos de número de arestas), algoritmo de Edmonds-Karp (caminho mínimo).
    Faz um bfs normal, mas também olha a capacidade residual (capacity - flow) de cada aresta.
    Tem complexidade O(V + A) de um bfs normal.
    Garantido que será chamada menos que VA/2 vezes, onde A é o número de arestas do grafo.
    Intuição da prova:
    - Arco crítico: em cada caminho aumentante, existe um arco que limita o aumento do fluxo (o que tem a menor capacidade residual).
    - Se um arco é crítico num caminho aumentador de comprimento k, 
      o próximo caminho aumentador no qual a é crítico tem comprimento pelo menos k+2.
    - O comprimento máximo dos caminhos é menor que V, logo cada arco pode ser crítico em no máximo V/2 caminhos aumentantes.
    - Logo, o número máximo de caminhos aumentantes é A * V/2 = VA/2.
    '''
    visited = [False] * graph.V
    parent = [(-1, None)] * graph.V

    fila = [source]
    visited[source] = True
    while fila:
        u = fila.pop(0)
        for node in graph.adj[u]:
            v = node.vertex
            if not visited[v] and node.capacity - node.flow > 0:
                visited[v] = True
                parent[v] = (u, node)
                if v == sink:
                    break
                fila.append(v)
        if visited[sink]:
            break

    if not visited[sink]:
        return -1, parent

    # Find the maximum flow through the path found.
    delta = sys.maxsize
    v = sink
    while v != source:
        u, node = parent[v]
        if node is None:
            continue
        delta = min(delta, node.capacity - node.flow)
        v = u

    return delta, parent


def max_cap_augmenting_path(graph, source, sink):
    '''
    Também sugerido por Edmonds-Karp (caminho-gordo).
    Busca pelo caminho aumentante com maior capacidade (capacity - flow), algoritmo similar ao de Dijkstra.
    Usa uma heap para sempre expandir o nó com maior capacidade residual.
    Número de caminhos encontrados nunca é maior que 2A*log(M), onde A é o número de arestas e M é a capacidade máxima do grafo.
    '''
    visited = [False] * graph.V
    parent = [(-1, None)] * graph.V
    cprd = [0] * graph.V

    heap = []
    cprd[source] = sys.maxsize
    heapq.heappush(heap, (-cprd[source], source))
    visited[source] = True

    while heap:
        cap_x, x = heapq.heappop(heap)
        cap_x = -cap_x

        if cap_x == 0 or x == sink:
            break

        for edge in graph.adj[x]:
            w = edge.vertex
            visited[w] = True
            capacity = edge.capacity
            flow = edge.flow
            residual = min(cprd[x], capacity - flow)
            if residual > cprd[w]:
                cprd[w] = residual
                parent[w] = (x, edge)
                heapq.heappush(heap, (-cprd[w], w))

    if not visited[sink] or cprd[sink] == 0:
        return -1, parent

    return cprd[sink], parent


if __name__ == "__main__":
    g = Graph(6, 8)
    g.add_edge(0, 1, 2)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 3)
    g.add_edge(1, 4, 1)
    g.add_edge(2, 3, 1)
    g.add_edge(2, 4, 1)
    g.add_edge(3, 5, 2)
    g.add_edge(4, 5, 3)

    source = 0
    sink = 5

    # g.print_flows(show_empty=True)
    # max_flow_dfs = g.get_max_flow(source, sink, dfs_augmenting_path)
    # print(f"Max Flow G DFS: {max_flow_dfs}")
    # max_flow = g.get_max_flow(source, sink, bfs_augmenting_path)
    # print(f"Max Flow G BFS: {max_flow}")
    # max_flow_maxcap = g.get_max_flow(source, sink, max_cap_augmenting_path)
    # print(f"Max Flow G Max-Cap: {max_flow_maxcap}")

    h = Graph(8, 15)  # 8 15
    h.add_edge(0, 1, 10)  # 1 2 10
    h.add_edge(0, 2, 5)  # 1 3 5
    h.add_edge(0, 3, 15)  # 1 4 15
    h.add_edge(1, 2, 4)  # 2 3 4
    h.add_edge(1, 4, 9)  # 2 5 9
    h.add_edge(1, 5, 15)  # 2 6 15
    h.add_edge(2, 3, 4)  # 3 4 4
    h.add_edge(2, 5, 8)  # 3 6 8
    h.add_edge(3, 6, 16)  # 4 7 16
    h.add_edge(4, 5, 15)  # 5 6 15
    h.add_edge(4, 7, 10)  # 5 8 10
    h.add_edge(5, 6, 15)  # 6 7 15
    h.add_edge(5, 7, 10)  # 6 8 10
    h.add_edge(6, 2, 6)  # 7 3 6
    h.add_edge(6, 7, 10)  # 7 8 10
    # max_flow_h_dfs = h.get_max_flow(0, 7, dfs_augmenting_path)
    # print(f"Max Flow H DFS: {max_flow_h_dfs}")
    # max_flow_h = h.get_max_flow(0, 7, bfs_augmenting_path)
    # print(f"Max Flow H BFS: {max_flow_h}")
    # max_flow_h_maxcap = h.get_max_flow(0, 7, max_cap_augmenting_path)
    # print(f"Max Flow H Max-Cap: {max_flow_h_maxcap}")

    f = Graph(10, 16)
    f.add_edge(0, 1, 5)
    f.add_edge(0, 2, 8)
    f.add_edge(0, 3, 3)
    f.add_edge(0, 4, 5)
    f.add_edge(0, 5, 7)
    f.add_edge(0, 9, 7)
    f.add_edge(1, 9, 4)
    f.add_edge(2, 9, 9)
    f.add_edge(3, 6, 1)
    f.add_edge(4, 7, 4)
    f.add_edge(5, 6, 1)
    f.add_edge(5, 7, 2)
    f.add_edge(5, 8, 6)
    f.add_edge(6, 9, 1)
    f.add_edge(7, 9, 6)
    f.add_edge(8, 9, 5)

    # max_flow_f_dfs = f.get_max_flow(0, 9, dfs_augmenting_path)
    # print(f"Max Flow F DFS: {max_flow_f_dfs}")
    # max_flow_f = f.get_max_flow(0, 9, bfs_augmenting_path)
    # print(f"Max Flow F BFS: {max_flow_f}")
    max_flow_f_maxcap = f.get_max_flow(0, 9, max_cap_augmenting_path)
    print(f"Max Flow F Max-Cap: {max_flow_f_maxcap}")
