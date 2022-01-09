
from src.Vertex import Vertex
from src.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    def __init__(self):
        self.Nodes = dict()
        self.Edges = dict()
        self.NumberOfEdges = 0
        self.MC = 0

    def __repr__(self):
        NumOfVs = str(self.v_size())
        NumOfEs = str(self.e_size())
        return "Graph: |V|=" + NumOfVs + " , |E|=" + NumOfEs

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        ################################################################################################################

        return len(self.Nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        ################################################################################################################

        return self.NumberOfEdges

    def get_all_v(self):
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        ################################################################################################################

        return self.Nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        ################################################################################################################

        node = self.Nodes[id1]
        ans = node.EdgesGoingInside
        return ans

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        ################################################################################################################

        return self.Nodes[id1].EdgesGoingOutside

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        ################################################################################################################

        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        ################################################################################################################

        if id1 not in self.Nodes \
                or id2 not in self.Nodes \
                or id1 == id2:
            return False

        self.Nodes[id1].EdgesGoingOutside[id2] = weight
        self.Nodes[id2].EdgesGoingInside[id1] = weight
        self.NumberOfEdges += 1
        self.MC += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        ################################################################################################################

        if node_id in self.Nodes:
            return False
        self.Nodes[node_id] = Vertex(node_id, pos)
        self.MC += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        ################################################################################################################

        if node_id not in self.Nodes:
            return False
        for key in self.Nodes[node_id].EdgesGoingInside.keys():
            if key in self.Nodes:
                self.Nodes[key].EdgesGoingOutside.pop(node_id)
                self.NumberOfEdges -= 1

        """
        Removing the given vertice and updating the # of edges and the MC variable.
        """
        self.Nodes.pop(node_id)
        self.NumberOfEdges -= 1
        self.MC += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        ################################################################################################################

        if node_id1 in self.Nodes[node_id2].EdgesGoingInside \
                or node_id2 in self.Nodes[node_id1].EdgesGoingInside:
            self.Nodes[node_id1].EdgesGoingOutside.pop(node_id2)
            self.Nodes[node_id2].EdgesGoingInside.pop(node_id1)
            self.NumberOfEdges -= 1
            self.MC += 1

            return True

        else:
            return False

    def getNode(self, id: int):
        if self.Nodes.__contains__(id):
            return self.Nodes.get(id)
