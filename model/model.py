import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.listAirports = []
        self.idMap = {}
        self.loadAirports()

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []

        self.solBest = []
        self.pesoMax = 0

    def loadAirports(self):
        self.listAirports = DAO.getAllAirports()
        for airport in self.listAirports:
            self.idMap[airport.ID] = airport

    def buildgraph(self, x):

        possibiliNodi = DAO.getAirportAndNumCompagnie()

        for airport in possibiliNodi:
            if airport[1] >= x:
                self.nodes.append(self.idMap[airport[0]])

        self.graph.add_nodes_from(self.nodes)

        edges = {}
        for n1 in self.nodes:
            for n2 in self.nodes:
                if n1 != n2:
                    peso = DAO.getPeso(n1.ID,n2.ID)
                    if peso != [] and peso[0] > 0:
                        if (n2, n1) not in edges.keys():
                            edges[(n1, n2)] = peso[0]
                            self.edges.append((n1, n2))

        for key,peso in edges.items():
            self.graph.add_edge(key[0], key[1], weight=peso)


    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()

    def get_sorted_edges(self):
        return sorted(self.graph.edges(data=True), key=lambda x: x[2]['weight'], reverse=True)

    def getSortedNeighbors(self, nStart):
        result = []
        vicini = self.graph.neighbors(nStart)
        for nNext in vicini:
            result.append((nNext, self.graph[nStart][nNext]['weight']))
        return sorted(result, key=lambda x: x[1], reverse=True)


    def calcPath(self, a1, a2, t):
        self.solBest = []
        self.pesoMax = 0
        print("entrato")
        self.ricorsione( a2, t, [a1])
        print("uscito")

    # il percorso che massimizzi la somma dei pesi degli archi attraversati, utilizzando al massimo t tratte.

    def ricorsione(self, nEnd, tratte, parziale):

        if len(parziale) > tratte +1:
            return

        if parziale[-1] == nEnd:
            pesoPercorso = self.calcolaPesoPercorso(parziale)
            if pesoPercorso > self.pesoMax:
                self.pesoMax = pesoPercorso
                self.solBest = list(parziale)
            return

        viciniAmm = self.cercaArchiAmm(parziale)

        for node in viciniAmm:
            parziale.append(node)
            self.ricorsione(nEnd, tratte, parziale)
            parziale.pop()

    def cercaArchiAmm(self, parziale):
        result = []
        nStart = parziale[-1]
        vicini = self.graph.neighbors(nStart)
        for nNext in vicini:
            if nNext not in parziale:
                result.append(nNext)
        return result

    def calcolaPesoPercorso(self, parziale):
        somma = 0
        for i in range(0, len(parziale) - 1):
            somma += self.graph[parziale[i]][parziale[i + 1]]["weight"]
        return somma

    def verificaConnesione(self, a1, a2):
        connessa = nx.node_connected_component(self.graph, a1)
        if a2 in connessa:
            return True
        return False





















