import os
import matplotlib.pyplot as plt
import math
import glob
import random
# from graphviz import Graph as GraphViz


class Graph:
    def __init__(self, V: int):
        self.V = V
        # List of lists to hold adjacency nodes
        self.adj = [[] for _ in range(V)]
        self.colors = {}
        self.names = {}
        self.inv_names = {}

    def add_edge(self, u: int, v: int):
        if u not in self.inv_names:
            self.names[str(u)] = u
            self.names[u] = str(u)

        if v not in self.inv_names:
            self.names[str(v)] = v
            self.names[v] = str(v)

        self.adj[u].append(v)
        self.adj[v].append(u)
        if u not in self.colors:
            self.colors[u] = -1
        if v not in self.colors:
            self.colors[v] = -1

    def add_named_edge(self, u: str, v: str):
        if not u in self.names:
            idx = len(self.names)
            self.names[u] = idx
            self.inv_names[idx] = u
        if not v in self.names:
            idx = len(self.names)
            self.names[v] = idx
            self.inv_names[idx] = v

        self.add_edge(self.names[u], self.names[v])

    def has_named_vertice(self, name: str) -> bool:
        return name in self.names

    def show_edges(self):
        for i in range(len(self.adj)):
            for j in self.adj[i]:
                print(f"{i}->{j}")
                print(f"{self.inv_names[i]} -> {self.inv_names[j]}")

    def bfs(self):
        print("Graph adjacency list:")

        visited = set([0])
        queue = [0]

        while len(queue) != 0:
            v = queue.pop(0)
            print(v)
            neighbors = self.adj[v]
            for neighbor in neighbors:
                if neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

    def draw(self, step):
        # Circular layout
        angles = [2 * math.pi * i / self.V for i in range(self.V)]
        positions = [(math.cos(a), math.sin(a)) for a in angles]
        fig, ax = plt.subplots(figsize=(4, 4))
        color_map = ['gray', 'red', 'green', 'blue', 'orange',
                     'purple', 'yellow', 'pink', 'cyan', 'brown']
        # Draw edges
        for u in range(self.V):
            for v in self.adj[u]:
                if u < v:
                    x1, y1 = positions[u]
                    x2, y2 = positions[v]
                    ax.plot([x1, x2], [y1, y2], color='black', zorder=1)
        # Draw nodes
        for v in range(self.V):
            x, y = positions[v]
            c = self.colors.get(v, -1)
            node_color = color_map[c] if c >= 0 else 'white'
            ax.scatter(x, y, s=600, color=node_color,
                       edgecolors='black', zorder=2)
            ax.text(x, y, str(v), ha='center',
                    va='center', fontsize=14, zorder=3)
        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-1.2, 1.2)
        ax.axis('off')
        ax.set_title(f"Step {step}")
        fig.tight_layout()
        # Salva PNG
        os.makedirs("frames3", exist_ok=True)
        fig.savefig(f"frames3/step_{step:03d}.png")
        plt.close(fig)

    # def draw_graphviz(self, step=0):
    #     color_map = ['gray', 'red', 'green', 'blue', 'orange',
    #                  'purple', 'yellow', 'pink', 'cyan', 'brown']
    #     dot = GraphViz()

    #     for node in self.names:
    #         color = self.colors[self.names[node]]
    #         dot.node(node, style='filled',
    #                  fillcolor=color_map[color] if color >= 0 else 'white')

    #     visited = {}

    #     for i in range(len(self.adj)):
    #         for j in self.adj[i]:
    #             if j not in visited:
    #                 dot.edge(self.inv_names[i], self.inv_names[j])
    #         visited[i] = True

    #     os.makedirs("frames3", exist_ok=True)
    #     png_data = dot.pipe(format='png')
    #     with open(f'frames3/step_{step:03d}.png', 'wb') as f:
    #         f.write(png_data)
    #     # file_path = os.path.join("frames3", f"step_{step:03d}")
    #     # dot.render(file_path, format='png')  # Cria e abre a imagem

    def _can_color_aux(self, k, v, step):
        if v == self.V:
            # self.draw_graphviz(step[0])
            return True

        for c in range(k):
            temVizinhoComMesmaCor = False

            for neighbor in self.adj[v]:
                if self.colors[neighbor] == c:
                    temVizinhoComMesmaCor = True
                    break

            if temVizinhoComMesmaCor:
                continue

            self.colors[v] = c

            step[0] += 1
            # self.draw_graphviz(step[0])
            if (self._can_color_aux(k, v + 1, step)):
                return True

            self.colors[v] = -1
            step[0] += 1
            # self.draw_graphviz(step[0])

    def can_color(self, k):
        files = glob.glob("frames3/*")
        for f in files:
            os.remove(f)

        print(self.adj)
        if self._can_color_aux(k, 0, [0]):
            print(self.colors)
            return True

        print("Não é possível")
        return False


# if __name__ == "__main__":
#     N = 15
#     g = Graph(N)
#     random.seed(42)

#     for u in range(N):
#         for v in range(u + 1, N):
#             if random.random() < 0.4:
#                 g.add_edge(u, v)

#     g.can_color(4)


if __name__ == "__main__":
    N = 30
    g = Graph(N)

    sat = [
        ["x1", "-x2", "x3"],
        ["-x1", "x2", "x4"],
        ["x1", "x3", "-x4"]
    ]

    # sat = [
    #     ["a", "b", "c"],
    #     ["-a", "-b", "-c"],
    #     ["a", "-b", "-c"],
    # ]

    # sat = [
    #     ["x", "y", "z"],
    #     ["x", "y", "-z"],
    #     ["x", "-y", "z"],
    #     ["x", "-y", "-z"],
    #     ["-x", "y", "z"],
    #     ["-x", "y", "-z"],
    #     ["-x", "-y", "z"],
    #     ["-x", "-y", "-z"]
    # ]

    g.add_named_edge("Base", "True")
    g.add_named_edge("Base", "False")
    g.add_named_edge("True", "False")

    for i in range(len(sat)):
        c = sat[i]
        for x in c:
            if g.has_named_vertice(x):
                continue

            pure_x = x.replace("-", "")

            g.add_named_edge("Base", pure_x)
            g.add_named_edge("Base", "-"+pure_x)
            g.add_named_edge(pure_x, "-"+pure_x)

        x1, x2, x3 = c
        g.add_named_edge(f"{x1}", f"aux_{i}_{x1}")
        g.add_named_edge(f"{x2}", f"aux_{i}_{x2}")
        g.add_named_edge(f"aux_{i}_{x1}", f"aux_{i}_{x2}")
        g.add_named_edge(f"aux_{i}_{x1}", f"{x1}V{x2}")
        g.add_named_edge(f"aux_{i}_{x2}", f"{x1}V{x2}")
        g.add_named_edge(f"{x1}V{x2}", f"aux_{x1}V{x2}")
        g.add_named_edge(f"{x3}", f"aux_{i}_{x3}")
        g.add_named_edge(f"aux_{i}_{x3}", f"aux_{x1}V{x2}")
        g.add_named_edge(f"aux_{i}_{x3}", f"{x1}V{x2}V{x3}")
        g.add_named_edge(f"aux_{x1}V{x2}", f"{x1}V{x2}V{x3}")
        g.add_named_edge(f"{x1}V{x2}V{x3}", "False")
        g.add_named_edge(f"{x1}V{x2}V{x3}", "Base")

    g.show_edges()

    g.can_color(3)
