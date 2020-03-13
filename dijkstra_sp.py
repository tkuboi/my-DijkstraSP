"""Contains Dijkstra's shortest path algorithm
CPE 202
"""
import sys
import traceback
from min_pq_special import MinPQ

class Vertex:
    """class for Vertex
    Attributes:
        key (int) : key
        val (int) : value
        edges (list) : a list of tuples of (Vertex, weight)
        predecessor (Vertex) : the predecessor
        dist (int) : the distnace
    """
    def __init__(self, key, val, num_edges):
        self.key = key
        self.val = val
        self.edges = [None] * (num_edges + 1)
        self.reset()

    def __repr__(self):
        return "Vertex: %s, %s" % (self.key, self.val)

    def __eq__(self, other):
        return isinstance(other, Vertex) and self.key == other.key\
            and self.val == other.val and self.edges == other.edges

    def __lt__(self, other):
        return self.dist < other.dist

    def add_edge(self, vertex, weight):
        """adds an edge to an vertex
        Args:
            vertex (Vertex) : the destination Vertex
            weight (int) : the weight of the edge
        """
        self.edges[vertex.key] = (vertex, weight)

    def get_edge(self, key):
        """gets a edge to a vertex with the given key
        Args:
            key (int): the key
        Returns:
            Vertex: the vertex with the key
            int: the weight of the edge
        """
        return self.edges[key]

    def get_edges(self):
        """returns a list of edges
        Returns:
            list : a list of tuples (Vertex, weight)
        """
        return [e for e in self.edges if e]

    def reset(self):
        """resets the vertex to the initial state.
        """
        self.predecessor = None
        self.dist = sys.maxsize #python's largest possible int value

class DijkstraSP:
    """A grpah for Dijkstra's shortest path
    Attributes:
        vertices (list) :  a list of Vertex
        num_vertices (int) : the number of vertices
        num_edges (int) : the number of edges
    """
    def __init__(self, filename=None, num_vertices=3):
        self.num_edges = 0
        self.pq = None 
        if filename:
            num_vertices, num_edges, vertices, edges = self.read_file(filename)
            self.num_vertices = num_vertices
            self.vertices = [None] * (self.num_vertices + 1)
            self.create_vertices(vertices)
            self.create_edges(edges)
        else:
            self.num_vertices = num_vertices
            self.vertices = [None] * (self.num_vertices + 1)

    def __repr__(self):
        return "num_vertices: %d, num_edges: %d, vertices: %s" % (
            self.num_vertices, self.num_edges, self.vertices)

    @staticmethod
    def read_file(filename):
        """read input file containing info about a graph.
        Args:
            filename (str): a path and filename
        Returns:
            int: the number of vertices
            int: the number of edges
            list: a list of tuples about vertices
            list: a list of tuples about edges
        """
        num_vertices = 0
        num_edges = 0
        vertices = []
        edges = []
        with open(filename) as inf:
            lines = inf.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                num_vertices = int(line.replace('\n', ''))
            elif i == 1:
                num_edges = int(line.replace('\n', ''))
            elif 1 < i <= 1 + num_vertices:
                vertices.append(
                    [int(v) if v.isnumeric() else v\
                        for v in line.replace('\n', '').split('\t')])
            else:
                edges.append(
                    [int(e) for e in line.replace('\n', '').split('\t')])
        return num_vertices, num_edges, vertices, edges

    def create_vertices(self, vertices):
        """create vertices
        Args:
            vertices (list): a list of tuples (key, name)
        """
        for key, val in vertices:
            self.add_vertex(key, val)

    def create_edges(self, edges):
        """create edges
        Args:
            edges (list): a list of tuples (source, destination, weight)
        """
        for source, dest, weight in edges:
            self.add_edge(source, dest, weight)

    def add_vertex(self, key, val=None):
        """adds an Vertex to the graph
        Args:
            key (int) : the key of the vertex
            val (any) : the value
        """
        vertex = Vertex(key, val, self.num_vertices)
        self.vertices[key] = vertex

    def get_vertex(self, key):
        """gets a vertex with the given key
        Args:
            key (int): the key
        Returns:
            Vertex: the vertex with the key
        """
        return self.vertices[key]

    def add_edge(self, org, dest, weight=1):
        """adds an edge between two vertices
        Args:
            org (int) : the key of the origin
            dest (int) : the key of the destination
            weight (int) : the weight of the edge
        """
        org_v = self.vertices[org]
        to_v = self.vertices[dest]
        org_v.add_edge(to_v, weight)
        to_v.add_edge(org_v, weight)
        self.num_edges += 1

    def reset_vertices(self):
        """resets vertices to the initial state
        """
        for vertex in self.vertices:
            if vertex is not None:
                vertex.reset()

    def dijkstra_sp(self, source):
        """find the shortest path from the source
        Args:
            source (int): key of the source vertex
        """
        self.pq = MinPQ(self.num_vertices + 1)
        source_vertex = self.vertices[source]
        source_vertex.predecessor = None
        source_vertex.dist = 0
        self.pq.insert(source_vertex)
        while not self.pq.is_empty():
            self.relax(self.pq.del_min())

    def relax(self, current):
        """updates the distance of vertices
        Args:
            current (Vertex): the vertex currently processed
        """
        for vertex, dist in current.get_edges():
            if vertex.dist > current.dist + dist:
                vertex.dist = current.dist + dist
                vertex.predecessor = current
                if self.pq.contains(vertex.key):
                    self.pq.change_key(vertex.key)
                else:
                    self.pq.insert(vertex)

    def shortest_path(self, source, dest):
        """finds the shortest path between two vertices
        Args:
            source (int): the key of source vertex
            dest (int): the key of the destination vertex
        Returns:
            int: the distance
            list: a list of tuples (src, dest, distnace)
        """
        self.dijkstra_sp(source)
        path = []
        dest = self.vertices[dest]
        dist = dest.dist
        while dest.predecessor:
            vertex, weight = dest.get_edge(dest.predecessor.key)
            path.append((dest.predecessor.val, dest.val, weight))
            dest = dest.predecessor
        return dist, path

    @staticmethod
    def print_path(path):
        """Prints a given path
        """
        idx = len(path) - 1
        while idx >= 0:
            src, dest, dist = path[idx]
            print("%s --> %s: %d miles" % (src, dest, dist))
            idx -= 1

    def print_vertices(self):
        """prints vertices in the graph.
        """
        for vertex in self.vertices:
            if vertex:
                print(vertex.key, vertex.val)
        print('')

def main():
    """create a graph from a given text file
    and find shortest path between apecified vertices
    using Dijkstra's algorithm.
    Prints the distance and the path on the screen.
    """
    if len(sys.argv) < 2:
        print("Usage: python3 dijkstra_sp.py [graph text file]")
        exit()
    filename = sys.argv[1]
    graph = DijkstraSP(filename)
    graph.print_vertices()

    while True:
        try:
            inp = input(
                "type Keys of the source and destination, or type q to quit:\n")
            if 'q' in inp:
                break
            graph.reset_vertices()
            tokens = inp.split()
            source_key, dest_key = int(tokens[0]), int(tokens[1])
            source = graph.get_vertex(source_key)
            dest = graph.get_vertex(dest_key)
            dist, path = graph.shortest_path(source_key, dest_key)
            print("The distance between %s and %s is %d miles." % (source.val, dest.val, dist))
            graph.print_path(path)
        except:
            traceback.print_exc(file=sys.stdout)
            print("Something went wrong. You probably pressed wrong keys.")

if __name__ == '__main__':
    main()
