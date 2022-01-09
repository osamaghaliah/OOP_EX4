from unittest import TestCase
from GraphAlgo import GraphAlgo
from DiGraph import DiGraph


class GraphAlgoTester(TestCase):

    def test_get_graph(self):
        Graph = DiGraph()
        for n in range(7):
            Graph.add_node(n)
        Graph.add_edge(0, 1, 1)
        Graph.add_edge(1, 0, 1.1)
        Graph.add_edge(1, 2, 1.3)
        Graph.add_edge(2, 3, 1.1)
        Graph.add_edge(1, 3, 10)
        Graph.add_edge(4, 5, 12)
        Graph.add_edge(3, 4, 22)
        Graph.add_edge(4, 6, 3)
        Graph.add_edge(6, 3, 18)
        graphAlgo = GraphAlgo(Graph)
        assert Graph is graphAlgo.get_graph()

    def test_SaveAndLoad(self):
        Graph = DiGraph()
        for n in range(7):
            Graph.add_node(n)
        Graph.add_edge(0, 1, 1)
        Graph.add_edge(1, 0, 1.1)
        Graph.add_edge(1, 2, 1.3)
        Graph.add_edge(2, 3, 1.1)
        Graph.add_edge(1, 3, 10)
        Graph.add_edge(4, 5, 12)
        Graph.add_edge(3, 4, 22)
        Graph.add_edge(4, 6, 3)
        Graph.add_edge(6, 3, 18)
        graphAlgo = GraphAlgo(Graph)

        # save the graph to a json file
        graphAlgo.save_to_json('Test.json')
        # Define another graph
        graphAlgoCopy = GraphAlgo()
        # load the graph that we saved before
        graphAlgoCopy.load_from_json('Test.json')

        # We should get a copy from the First Graph
        for i in Graph.get_all_v():
            assert graphAlgo.get_graph().get_all_v().get(i).getKey() is graphAlgoCopy.get_graph().get_all_v().get(i).getKey()

        # Check MC , Vertices_size , Edge_Size
        assert graphAlgo.get_graph().get_mc() is graphAlgoCopy.get_graph().get_mc()
        assert graphAlgo.get_graph().v_size() is graphAlgoCopy.get_graph().v_size()
        assert graphAlgo.get_graph().e_size() is graphAlgoCopy.get_graph().e_size()

    def test_shortest_path(self):
        Graph = DiGraph()
        for n in range(7):
            Graph.add_node(n)
        Graph.add_edge(0, 1, 1)
        Graph.add_edge(1, 0, 1.1)
        Graph.add_edge(1, 2, 1.3)
        Graph.add_edge(2, 3, 1.1)
        Graph.add_edge(1, 3, 10)
        Graph.add_edge(4, 5, 12)
        Graph.add_edge(3, 4, 22)
        Graph.add_edge(4, 6, 3)
        Graph.add_edge(6, 3, 18)
        graphAlgo = GraphAlgo(Graph)
        Src_Dest = graphAlgo.shortest_path(0, 3)
        assert True is (Src_Dest[0] == 3.4)
        ls = [0, 1, 2, 3]
        for i in Src_Dest[1]:
            assert True is (i == ls[i])

    def test_TSP(self):
        Graph = DiGraph()
        for n in range(5):
            Graph.add_node(n)
        Graph.add_edge(0, 1, 1)
        Graph.add_edge(0, 4, 5)
        Graph.add_edge(1, 0, 1.1)
        Graph.add_edge(1, 2, 1.3)
        Graph.add_edge(1, 3, 1.9)
        Graph.add_edge(2, 3, 1.1)
        Graph.add_edge(3, 4, 2.1)
        Graph.add_edge(4, 2, .5)
        GAlgoV1 = GraphAlgo(Graph)
        resultV1 = GAlgoV1.TSP([1, 2, 4])[0]
        costV1 = GAlgoV1.TSP([1, 2, 4])[1]
        actualV1 = [1, 2, 3, 4]
        actualCostV1 = 4.5
        assert resultV1 == actualV1
        assert costV1 == actualCostV1

        GAlgoV2 = GraphAlgo()
        GAlgoV2.load_from_json('../data/A5.json')
        resultV2 = GAlgoV2.TSP([1, 2, 3])[0]
        costV2 = GAlgoV2.TSP([1, 2, 3])[1]
        actualV2 = [1, 9, 2, 3]
        actualCostV2 = 2.370613295323088
        assert resultV2 == actualV2
        assert costV2 == actualCostV2