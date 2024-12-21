import random

# Class for an undirected graph
class Graph:
    # self.edges is a dictionary from vertices to the set
    # of adjacent vertices.

    # adjacencies is a list of pairs of vertex names.
    def __init__(self, adjacencies=None):
        self.edges = {}
        if adjacencies is not None:
            for pair in adjacencies:
                self.add_edge(pair)

    # Does someone want to try to write a better
    # printing function?
    def __str__(self):
        return str(self.edges)

    def add_edge(self, pair):
        if pair[0] == pair[1]:
            raise ValueError("A node cannot be connected to itself.")
        for (node1, node2) in [pair, reversed(pair)]:
            self.add_vertex(node1)
            self.edges[node1].add(node2)

    # Add an isolated vertex.
    def add_vertex(self, vertex):
        if vertex not in self.edges:
            self.edges[vertex] = set()

    def get_vertices(self):
        return list(self.edges.keys())

    def get_neighbors(self, vertex):
        return self.edges[vertex]

    def get_edges(self):
        output = set()
        for (node1, neighbors) in self.edges.items():
            for node2 in neighbors:
                output.add(tuple(sorted((node1, node2))))
        return list(output)

    def get_num_vertices(self):
        return len(self.edges)

    def get_num_edges(self):
        return len(self.get_edges())

    def is_empty(self):
        return not self.get_vertices()


# Code for generating sample graphs
# *********************************
# Namers: functions for generating vertex names.
# Vertex names A, B, C,... The default.


# Vertex names V_1, V_2,... No upper limit on number of vertices.
def general_vertex_namer(n):
    return "V_" + str(n - 1)


def letter_vertex_namer(n):
    if n > 26:
        raise ValueError("There are only 26 vertex letter names.")
    return chr(n + 64)


# A vertex namer for bipartite graphs.
def bipartite_namer(n, type):
    letter = "A" if type == 0 else "B"
    return letter + "_" + str(n)


def make_cycle_graph(n, vertex_namer=letter_vertex_namer):
    if n > 26:
        vertex_namer = general_vertex_namer
    adjacencies = []
    for i in range(1, n):
        adjacencies.append((vertex_namer(i), vertex_namer(i + 1)))
    adjacencies.append((vertex_namer(1), vertex_namer(n)))
    return Graph(adjacencies)


def make_complete_graph(n, vertex_namer=letter_vertex_namer):
    if n > 26:
        vertex_namer = general_vertex_namer
    adjacencies = []
    for i in range(1, n + 1):
        for j in range(1, i):
            adjacencies.append((vertex_namer(i), vertex_namer(j)))
    return Graph(adjacencies)


def make_complete_bipartite_graph(n, m, vertex_namer=bipartite_namer):
    adjacencies = []
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            adjacencies.append((vertex_namer(i, 0), vertex_namer(j, 1)))
    return Graph(adjacencies)


def make_random_graph(n, edge_probability=0.5,
                      vertex_namer=letter_vertex_namer):
    if n > 26:
        vertex_namer = general_vertex_namer
    adjacencies = []
    for i in range(1, n + 1):
        for j in range(1, i):
            if random.uniform(0, 1) < edge_probability:
                adjacencies.append((vertex_namer(i), vertex_namer(j)))
    my_graph = Graph(adjacencies)
    for i in range(1, n + 1):
        my_graph.add_vertex(vertex_namer(i))
    return my_graph


if __name__ == '__main__':
    my_graph = Graph([(3,4), (4,5)])
    print(my_graph)
