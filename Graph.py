import json
import os

import networkx as nx
import requests
from matplotlib import pyplot as plt


class Graph:
    def __init__(self):
        self.graph = nx.Graph()
        self.load_graph()

    def load_graph(self):
        if os.path.exists("./champion_graph.gml"):
            self.graph = nx.read_gml("champion_graph.gml")
        else:
            self.graph = nx.Graph()
            self.add_champions_to_graph()
            self.save_graph()

    def save_graph(self):
        nx.write_gml(self.graph, "champion_graph.gml")
        print(self.graph)

    def add_champions_to_graph(self):
        champs = json.loads(
            requests.get("https://ddragon.leagueoflegends.com/cdn/14.7.1/data/en_US/champion.json").content)
        champs_data = champs["data"]
        #for champ in champs_data:
        for champ in ["Teemo", "Jax", "Kennen", "MissFortune", "Rell"]:
            self.graph.add_node(champ)

    def add_team_comp_to_graph(self, champs):
        for champ in champs:
            for champ_2 in champs:
                if champ == champ_2: continue
                if self.graph.has_edge(champ, champ_2):
                    self.graph.get_edge_data(champ, champ_2)["weight"] += 1
                else:
                    self.graph.add_edge(champ, champ_2, weight=1)
        self.save_graph()

    def draw_graph(self):
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)
        plt.show()


if __name__ == "__main__":
    graph = Graph()
    graph.add_team_comp_to_graph(["Teemo", "Jax", "Kennen", "MissFortune", "Rell"])
    graph.draw_graph()