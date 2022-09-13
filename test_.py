from dijkstra_sp import DijkstraSP

def test():
    """create a graph from a given text file
    and find shortest path between apecified vertices
    using Dijkstra's algorithm.
    Prints the distance and the path on the screen.
    """
    filename = 'graph1.txt'
    graph = DijkstraSP(filename)
    graph.print_vertices()

    source_key = 1 
    dest_key = 9
    source = graph.get_vertex(source_key)
    assert source == 'Los Angeles'
    dest = graph.get_vertex(dest_key)
    assert dest == 'San Francisco'
    dist, path = graph.shortest_path(source_key, dest_key)
    assert dist == 300

