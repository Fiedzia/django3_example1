import json
from django.test import Client, TestCase
from webapp.models import NetworkConnectivity

class RoutingTestCase(TestCase):
    def setUp(self):
        NetworkConnectivity.objects.create(node_from=1, node_to=2)
        NetworkConnectivity.objects.create(node_from=2, node_to=3)

    def test_routing(self):
        client = Client()
        resp = client.get('/route/', {'node_from': '1', 'node_to': '3'})
        self.assertEqual(json.loads(resp.content), [1, 2, 3])

    def test_routing_same_node(self):
        client = Client()
        resp = client.get('/route/', {'node_from': '1', 'node_to': '1'})
        self.assertEqual(json.loads(resp.content), [1])

    def test_routing_invalid_node(self):
        client = Client()
        resp = client.get('/route/', {'node_from': '1', 'node_to': '5'})
        self.assertEqual(resp.status_code, 400)

