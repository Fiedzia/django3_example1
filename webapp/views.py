from django.http import HttpResponse, JsonResponse

import networkx

from .routing import load_graph


def index(request):
    """
    Generate routing for given nodes
    """
    graph = load_graph()

    try:
        node_from = int(request.GET['node_from'])
        node_to = int(request.GET['node_to'])
        path = networkx.shortest_path(graph, node_from, node_to)
        return JsonResponse(path, safe=False)
    except networkx.exception.NodeNotFound as e:
        # sending unknown nodes is treated as invalid request
        return HttpResponse('unknown nodes: ' + str(e), status=400)
