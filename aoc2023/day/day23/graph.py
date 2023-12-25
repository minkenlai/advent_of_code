from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.graph = defaultdict(list)
        self.V = vertices

    def add_edge(self, u, v, weight):
        self.graph[u].append((v, weight))

    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        if v in self.graph:
            for node, _ in self.graph[v]:
                if not visited[node]:
                    self.topological_sort_util(node, visited, stack)
        stack.append(v)

    def topological_sort(self):
        visited = {v: False for v in range(self.V)}
        stack = []

        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)

        return stack[::-1]

    def longest_path(self, s):
        dist = [-float('inf')] * self.V
        dist[s] = 0

        top_order = self.topological_sort()

        for node in top_order:
            if dist[node] != -float('inf'):
                for neighbor, weight in self.graph[node]:
                    if dist[neighbor] < dist[node] + weight:
                        dist[neighbor] = dist[node] + weight

        return dist


def test():
    # Example usage:
    g = Graph(6)
    g.add_edge(0, 1, 5)
    g.add_edge(0, 2, 3)
    g.add_edge(1, 3, 6)
    g.add_edge(1, 2, 2)
    g.add_edge(2, 4, 4)
    g.add_edge(2, 5, 2)
    g.add_edge(2, 3, 7)
    g.add_edge(3, 5, 1)
    g.add_edge(3, 4, -1)
    g.add_edge(4, 5, -2)

    source_vertex = 1
    result = g.longest_path(source_vertex)

    for i in range(len(result)):
        print(f"Distance from {source_vertex} to {i}: {result[i]}")

if __name__=='__main__':
    test()