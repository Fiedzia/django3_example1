import networkx

from webapp.models import NetworkConnectivity


def load_graph() -> networkx.Graph:
    """
    Load full graph data from database
    """
    graph = networkx.Graph()
    edges = NetworkConnectivity.objects.all()
    for edge in edges:
        graph.add_edge(edge.node_from, edge.node_to)
    return graph
