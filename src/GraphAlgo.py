from src.DiGraph import DiGraph
from src.GraphInterface import GraphInterface
from src.GraphAlgoInterface import GraphAlgoInterface
from typing import List
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
import sys
import json


class GraphAlgo(GraphAlgoInterface):
    def __init__(self, Graph = DiGraph()):
        self.Graph = Graph

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        ################################################################################################################

        return self.Graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        ################################################################################################################

        self.Graph = DiGraph()
        try:
            with open(file_name) as json_file:
                GraphLoading = json.load(json_file)

                """
                Reaching every node and adding it into the graph
                """
                for node in GraphLoading['Nodes']:
                    self.Graph.add_node(node['id'])
                    if 'pos' in node:
                        pos = node['pos'].split(',')
                        self.Graph.Nodes[node['id']].pos = [float(x) for x in pos]

                """
                Reaching every edge and adding it into the graph
                """
                for edge in GraphLoading['Edges']:
                    src = edge['src']
                    dest = edge['dest']
                    weight = edge['w']
                    self.Graph.add_edge(src, dest, weight)
        except FileNotFoundError:
            print("Error occured: " + file_name + " doesn't exist!")
            return False
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        ################################################################################################################

        GraphWriting = {"Nodes": [], "Edges": []}
        for node in self.Graph.Nodes.values():
            pp = {"id": node.getKey()}

            """
            Analyzing each node's X/Y/Z attributes (Place), and then writing it to the file.
            """
            if node.pos is not None:
                pp["pos"] = str(node.pos[0]) + "," + str(node.pos[1]) + "," + str(node.pos[2])

            GraphWriting["Nodes"].append(pp)

            """
            Analyzing each node's edges, source, destination and weight, and then writing it to the file.
            """
            for destKey, weight in node.EdgesGoingOutside.items():
                GraphWriting["Edges"].append({"src": node.getKey(), "dest": int(destKey), "w": weight})

        try:
            with open(file_name, 'w') as json_file:
                json.dump(GraphWriting, json_file)
                return True
        except FileNotFoundError:
            print("Writing a JSON file attempt has failed!")
            return False

    def getIndex(self, d: list, q: list) -> int:
        index = 0
        MIN = sys.maxsize
        for i, item in enumerate(d):
            if item <= MIN and i in q:
                MIN = item
                index = i
        return index

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        """
        ################################################################################################################

        MyList = []
        """
        Checking if the given do exist.
        """
        if self.Graph.Nodes.get(id1, -1) == -1 or self.Graph.Nodes.get(id2, -1) == -1:
            MyList.append(float('inf'))
            MyList.append([])
            return (MyList)

        MyList = []
        prev = []
        dist = []

        """
        Initially, all vertices are unvisited, so v[i] for all i is unvisited and as no path is yet paved.
        dist[i] for all i set to infinity.
        """
        for i in range(max(self.Graph.get_all_v()) + 1):
            dist.insert(i, sys.maxsize)
            prev.insert(i, -1)

        for key, value in self.Graph.get_all_v().items():
            MyList.append(key)

        """
        Now, source is first to be visited and distance from source to itself should be 0
        """
        dist[id1] = 0
        while len(MyList) != 0:
            index = self.getIndex(dist, MyList)
            MyList.remove(index)

            for n, weight in self.Graph.all_out_edges_of_node(index).items():
                if n in MyList:
                    alt = dist[index] + weight
                    if alt < dist[n]:
                        dist[n] = alt
                        prev[n] = index

        dest = id2
        MyListV1 = []
        MyListV2 = []
        i = 0

        if prev[dest] != -1 or id1 == dest:
            while dest != -1:
                MyListV1.insert(i, dest)
                i += 1
                dest = prev[dest]

        if i == 1 or dist[id2] == sys.maxsize:
            MyList.append(float('inf'))
            MyList.append([])

            return MyList

        else:
            i -= 1

            while i >= 0:
                MyListV2.append(MyListV1[i])
                i -= 1
            MyList.append(dist[id2])
            MyList.append(MyListV2)

        return MyList

    def Sp_Cost(self, s, e) -> (list, float):
        """
        Helping function for TSP, returns list of nodes and the cost of destination.
        """
        lst = self.shortest_path(s, e)[1]
        cost = self.shortest_path(s, e)[0]

        return lst, cost

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        ################################################################################################################

        if node_lst is None:
            return None, None
        
        else:
            cost = 0
            TheRequestedPathToGoOver = []
            Starting = node_lst[0]

            """
            Looping over the given vertices list and starting the correct operations.
            """
            indV1 = 1
            while indV1 < len(node_lst):
                Ending = node_lst[indV1]

                """
                Determining cost and path of vertices by calling shortest_path function.
                And inserting "Starting" as a source parameter and "Ending" as a destination parameter.
                """
                ShortestPathsCollection = self.Sp_Cost(Starting, Ending)[0]
                cost = cost + self.Sp_Cost(Starting, Ending)[1]
                Starting = Ending
                indV1 += 1

                """
                Deciding what vertices to take by looping over "ShortestPathsCollections" that was
                made in the previous stage. Then we build the requested TSP algorithm - the set of vertices.
                a.k.a TheRequestedPathToGoOver 
                """
                indV2 = 0
                while indV2 < len(ShortestPathsCollection):
                    sp = ShortestPathsCollection[indV2]

                    if sp not in TheRequestedPathToGoOver:
                        TheRequestedPathToGoOver.append(sp)

                    indV2 += 1

            return TheRequestedPathToGoOver, cost

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        ################################################################################################################

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        ################################################################################################################

        """
        Setting up the whole figure's background color.
        """
        fig = plt.figure()
        fig.patch.set_facecolor('beige')
        ax = plt.axes()
        ax.set_facecolor('beige')

        """
        Setting up my graph's nodes and their attributes - Number of edges that are --> in & out.
        """
        minX = 0
        maxX = 0
        nodes_copy = []
        nodes = [v for v in self.Graph.Nodes.values()]

        for n in nodes:
            """
            Making the plot to generate random nodes everytime we run check0() in main.py
            """
            Randomization = [r for r in nodes_copy if r in n.EdgesGoingOutside or r in n.EdgesGoingInside]
            if n.pos is None:
                if len(Randomization) < 1:
                    n.pos = np.random.random(2) * np.array([100, 100])
                else:
                    n.pos = np.mean([r.pos for r in Randomization], 0)

            minX = min(minX, n.pos[0])
            maxX = max(maxX, n.pos[0])
            nodes_copy.append(n)

        """
        Graph presentation stage.
        """
        nodes = {n.getKey(): n for n in nodes_copy}
        for n in nodes.values():
            """
            Presenting the correct edges and their directions, by relating them to the nodes places.
            """
            for o in n.EdgesGoingOutside.keys():
                dx = nodes[o].pos[0] - n.pos[0]
                dy = nodes[o].pos[1] - n.pos[1]
                d = np.sqrt(np.square(dx) + np.square(dy))
                plt.arrow(n.pos[0], n.pos[1], dx, dy, edgecolor='beige', facecolor='beige', length_includes_head=True,
                          head_width=d * 0.02, head_length=d * 0.02, width=0.00001 / 100,
                          path_effects=[path_effects.Stroke(linewidth=3, foreground='darkred'), path_effects.Normal()])

            plt.text(n.pos[0] + .0, n.pos[1], n.getKey(), font='Comic Sans MS', fontsize=9, fontweight='bold',
                     color='beige',
                     path_effects=[path_effects.Stroke(linewidth=3, foreground='black'), path_effects.Normal()])

            """
            Presenting the graph nodes according to their specified X & Y axes.
            """
            for n in nodes.values():
                plt.plot(n.pos[0], n.pos[1], 'o', color='beige', markersize=5,
                         path_effects=[path_effects.Stroke(linewidth=6, foreground='black'), path_effects.Normal()])

        """
        Creating and beautifying the GUI's title.
        """
        plt.title('Directed Weighted Graph - G.U.I', fontsize=16, color='beige', font='Copperplate Gothic Light',
                  fontweight='bold', path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                                                   path_effects.Normal()])

        """
        Creating and beautifying the GUI's X Axis.
        """
        plt.xlabel('X Axis', fontsize=16, color='beige', font='Copperplate Gothic Light',
                   fontweight='bold', path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                                                    path_effects.Normal()])

        """
        Creating and beautifying the GUI's Y Axis.
        """
        plt.ylabel('Y Axis', fontsize=16, color='beige', font='Copperplate Gothic Light',
                   fontweight='bold', path_effects=[path_effects.Stroke(linewidth=2, foreground='black'),
                                                    path_effects.Normal()])

        plt.show()
