"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

# init pygame
from src.DiGraph import DiGraph
from src.GraphAlgo import GraphAlgo

WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

clock = pygame.time.Clock()
pygame.font.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
BackgroundPNG = pygame.image.load("C:\\Users\\osama\\PycharmProjects\\Ex4\\Tools\\Background.png").convert()
mixer.init()
mixer.music.load('C:\\Users\\osama\\PycharmProjects\\Ex4\\Tools\\Soundtrack.ogg')
mixer.music.play()

client = Client()
client.start_connection(HOST, PORT)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

print(pokemons)

graph_json = client.get_graph()

FONT = pygame.font.SysFont('comicsansms', 18, bold=True)
# load the json string into SimpleNamespace Object

graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""

while client.is_running() == 'true':
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))
    screen.blit(BackgroundPNG, [0, 0])
    # draw nodes
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)


        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(178, 34, 34))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y), width=2)

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(0, 0, 255),
                           (int(agent.pos.x), int(agent.pos.y)), 10)

    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos.x), int(p.pos.y)), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    g = DiGraph()
    for n in graph.Nodes:
        src_x = my_scale(n.pos.x, x=True)
        src_y = my_scale(n.pos.y, y=True)
        t = (src_x, src_y)
        g.add_node(n.id, t)

    for e in graph.Edges:
        s = g.getNode(e.src).pos
        s1 = g.getNode(e.dest).pos
        w = ((((s[0] - s1[0]) ** 2) + ((s[1] - s1[1]) ** 2)) ** 0.5)
        g.add_edge(e.src, e.dest, w)

    gr = GraphAlgo(g)

    print(pokemons)

    def TargetedNode(pok):
        for e in graph.Edges:
            # find the edge nodes
            src = next(n for n in graph.Nodes if n.id == e.src)
            dest = next(n for n in graph.Nodes if n.id == e.dest)

            src_x = my_scale(src.pos.x, x=True)
            src_y = my_scale(src.pos.y, y=True)
            dest_x = my_scale(dest.pos.x, x=True)
            dest_y = my_scale(dest.pos.y, y=True)

            #d2 must equal d2, and an epsilon range were compared for determenation.
            d1 = abs(((((src_x - dest_x) ** 2) + ((src_y - dest_y) ** 2)) ** 0.5))
            d2 = abs(((((src_x - pok.x) ** 2) + ((src_y - pok.y) ** 2)) ** 0.5)) \
                 + abs(((((dest_x - pok.x) ** 2) + ((dest_y - pok.y) ** 2)) ** 0.5))

            if d1 > d2 - 0.000001:
                return dest.id, src.id

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            AgentPathToEatThePok = []
            AgentPathToEatThePok.append(agent.src)

            for pok in pokemons:
                target = TargetedNode(pok.pos)
                lst = gr.shortest_path(AgentPathToEatThePok[len(AgentPathToEatThePok) - 1], target[0])[1]
                lst.append(target[1])

                for index in lst:
                    AgentPathToEatThePok.append(index)

            for v in AgentPathToEatThePok:
                next_node = v
                client.choose_next_edge(
                    '{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(next_node) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()

# game over:
