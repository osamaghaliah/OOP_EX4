from src.GraphAlgo import GraphAlgo


def A0():
    Graph = GraphAlgo()
    Graph.load_from_json('../data/A0')
    Graph.plot_graph()


def A1():
    Graph = GraphAlgo()
    Graph.load_from_json('../data/A1')
    Graph.plot_graph()


def A2():
    Graph = GraphAlgo()
    Graph.load_from_json('../data/A2')
    Graph.plot_graph()


def A3():
    Graph = GraphAlgo()
    Graph.load_from_json('../data/A3')
    Graph.plot_graph()


if __name__ == '__main__':
    """
    The whole given graphs presentation. A0 to A5
    """

    A0()
    A1()
    A2()
    A3()
