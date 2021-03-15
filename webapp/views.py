import networkx

from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.db.models import Q

from .models import NetworkConnectivity


class ResourceLimitExceeded(Exception):
    pass


# protect from changing graph while we query it
@transaction.atomic
def index(request):
    """
    Generate routing for given nodes

    max_nodes/max_edges sets a limit on how much data
    we are allowed to load from db, if exceeded we return an error

    """
    graph = networkx.Graph()
    #do not load excessive amount of data from db
    max_nodes = 1000
    max_edges = 1000

    node_from = int(request.GET['node_from'])
    node_to = int(request.GET['node_to'])
    unknown_nodes = set([node_from, node_to])
    known_nodes = set([node_from, node_to])
    fully_loaded = False
    try:
        while True:
            for node in unknown_nodes.copy():
                known_nodes.add(node)
                unknown_nodes.remove(node)

                for edge in (NetworkConnectivity
                .objects
                .filter(Q(node_from=node) | Q(node_to=node))):

                    graph.add_edge(edge.node_from, edge.node_to)
                    if len(graph.edges) > max_edges:
                        raise ResourceLimitExceeded
                    if len(graph.nodes) > max_nodes:
                        raise ResourceLimitExceeded

                    known_nodes.add(node)
                    if edge.node_from not in known_nodes:
                        unknown_nodes.add(edge.node_from)
                    if edge.node_to not in known_nodes:
                        unknown_nodes.add(edge.node_to)
            if not unknown_nodes:
                fully_loaded = True
            try:
                path = networkx.shortest_path(graph, node_from, node_to)
                return JsonResponse(path, safe=False)

            except networkx.exception.NodeNotFound as e:
                if fully_loaded:
                    return HttpResponse('unknown node: ' + str(e), status=400)
                else:
                    pass
            except networkx.exception.NetworkXNoPath as e:
                if fully_loaded:
                    return HttpResponse('No path has been found between nodes', status=400)
                else:
                    pass
    except ResourceLimitExceeded:
        return HttpResponse('No path has been found within given node/edge limit', status=400)
