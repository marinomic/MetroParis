from geopy.distance import distance
from database.DAO import DAO
import networkx as nx


class Model:
    def __init__(self):
        self._fermate = DAO.getAllFermate()
        self._grafo = nx.DiGraph()
        self._idMap = {}
        for f in self._fermate:
            self._idMap[f.id_fermata] = f
        self._linee = DAO.getAllLinee()
        self._lineaMap = {}
        for l in self._linee:
            self._lineaMap[l.id_linea] = l

    def buildGraph(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.addEdgeMode3()

    def buildGraphPesato(self):
        self._grafo.clear()
        self._grafo.add_nodes_from(self._fermate)
        self.getEdgesPesatiLinee()

    def getNodesNumber(self):
        return len(self._grafo.nodes)

    def getEdgesNumber(self):
        return len(self._grafo.edges)

    @property
    def fermate(self):
        return self._fermate

    def addEdgeMode1(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            for v in self._fermate:
                res = DAO.getEdge(u, v)
                if len(res) > 0:
                    self._grafo.add_edge(u, v)
                    # print(f"Aggiunto arco tra {u.nome} e {v.nome}")

    def addEdgeMode2(self):
        self._grafo.clear_edges()
        for u in self._fermate:
            vicini = DAO.getEdgesVicini(u)
            for v in vicini:
                v_nodo = self._idMap[v["id_stazA"]]
                self._grafo.add_edge(u, v_nodo)

    def addEdgeMode3(self):
        self._grafo.clear_edges()
        allConn = DAO.getEdges()
        for c in allConn:
            # aggiunge gli archi composti dalle fermate di partenza e arrivo
            u = self._idMap[c.id_stazP]
            v = self._idMap[c.id_stazA]
            self._grafo.add_edge(u, v)

    # Meglio BFS per trovare i nodi raggiungibili
    def cercaRaggiungibili_BFS(self, source):
        # Implementare la ricerca dei nodi raggiungibili a partire dalla fermata di partenza, prima con la visita in ampiezza
        edges = nx.bfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    # Meglio DFS per trovare le componenti connesse
    def cercaRaggiungibili_DFS(self, source):
        # Implementare la ricerca dei nodi raggiungibili a partire dalla fermata di partenza, poi con la visita in profondità
        edges = nx.dfs_edges(self._grafo, source)
        visited = []
        for u, v in edges:
            visited.append(v)
        return visited

    # archi pesati secondo la prima parte del progetto
    def addEdgesPesati(self):
        """Questo metodo assegna come peso degli edges il numero di linee che congiungono i diversi nodi.
        """
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConn()
        for c in allConnessioni:
            if self._grafo.has_edge(self._idMap[c.id_stazP],
                                    self._idMap[c.id_stazA]):
                self._grafo[self._idMap[c.id_stazP]][self._idMap[c.id_stazA]]["weight"] += 1
            else:
                self._grafo.add_edge(self._idMap[c.id_stazP], self._idMap[c.id_stazA], weight=1)

    # archi pesati per i cammini minimi, secondo la seconda parte del progetto
    def getEdgesPesatiLinee(self):
        """
        Restuisce gli archi pesati secondo il tempo di percorrenza di ciascuna tratta considerando la velocità media
         della linea che connette le due fermate (Linea.velocita) e la distanza tra le stazioni in linea d'aria (Fermata.coords).
        """
        self._grafo.clear_edges()
        allConnessioni = DAO.getAllConn()
        for c in allConnessioni:
            v0 = self._idMap[c.id_stazP]
            v1 = self._idMap[c.id_stazA]
            linea = self._lineaMap[c.id_linea]
            peso = self.getTraversalTime(v0, v1, linea)
            # se ho già un arco tra v0 e v1 verifico che ci impieghi meno tempo
            #  Nel caso in cui due stazioni siano connesse da più linee, si considera quella più veloce.
            if self._grafo.has_edge(v0, v1):
                if self._grafo[v0][v1]["weight"] > peso:
                    self._grafo[v0][v1]["weight"] = peso
            else:
                self._grafo.add_edge(v0, v1, weight=peso)

    def getEdgeWeight(self, u, v):
        return self._grafo[u][v]["weight"]

    def getArchiPesoMaggiore(self):
        """Print di archi con peso maggiore di 1 (agisce solo sul grafo pesato)
        """
        if len(self._grafo.edges) == 0:
            print("Il grafo è vuoto")
            return

        edges = self._grafo.edges
        result = []

        for u, v in edges:
            peso = self._grafo[u][v]["weight"]
            if peso > 1:
                result.append((u, v, peso))
        return result

    @staticmethod
    def getTraversalTime(v0, v1, linea):
        p0 = (v0.coordX, v0.coordY)
        p1 = (v1.coordX, v1.coordY)
        distanza = distance(p0, p1).km
        vel = linea.velocita
        tempo = distanza / vel * 60  # tempo in minuti
        return tempo

    # calcola il percorso migliore tra due fermate utilizzando l'algoritmo di Dijkstra
    # per ottenere la lista dei nodi percorsi per raggiungere la destinazione, come richiesto dalla traccia
    def getBestPath(self, source, target):
        """
        Calcola il percorso migliore tra due fermate utilizzando l'algoritmo di Dijkstra.
        """
        path = nx.dijkstra_path(self._grafo, source, target, weight="weight")
        return path

    # se volessi ottenere anche il costo minimo (tempo totale) per raggiungere la destinazione, posso utilizzare la funzione nx.dijkstra_path_length
    # oppure direttamente nx.single_source_dijkstra(self._grafo, source, target) che appunto mi
    # restituisce sia il costo minimo che il percorso (in quest'ordine in una tupla) per raggiungere la destinazione.
    def getBestPathAndCost(self, source, target):
        """
        Calcola il percorso migliore tra due fermate utilizzando l'algoritmo di Dijkstra e restituisce il costo minimo per raggiungere la destinazione.
        """
        costoTot, path = nx.single_source_dijkstra(self._grafo, source, target)
        return round(costoTot, 3), path


"""
Quando si utilizzano solo gli identificativi (ID) per aggiungere nodi al grafo, ogni ID viene considerato un nodo distinto.
 Se si aggiungono gli ID direttamente, senza utilizzare un meccanismo di mappatura come self._idMap, e si hanno connessioni che coinvolgono 
 gli stessi nodi più volte, il grafo tratterà ogni occorrenza di un ID come un nodo separato, a meno che non si stia utilizzando esplicitamente
  un controllo per evitare duplicati prima di aggiungerli.  D'altra parte, utilizzando self._idMap per mappare ogni ID a un oggetto Fermata unico
   e aggiungendo questi oggetti al grafo, si garantisce che ogni nodo sia unico nel grafo, indipendentemente dal numero di volte che appare in
    connessioni diverse. Questo perché networkx identifica i nodi basandosi sull'oggetto stesso (in questo caso, l'istanza di Fermata), e non 
    sul valore dell'ID. Pertanto, anche se due fermate hanno lo stesso ID, saranno trattate come lo stesso nodo nel grafo se si utilizza l'oggetto
     Fermata mappato da self._idMap.  Se si osserva un raddoppio nel numero di nodi quando si utilizzano solo gli ID, è probabile che ciò sia dovuto
      al fatto che ogni ID viene considerato un nodo separato ogni volta che viene aggiunto al grafo, senza verificare se l'ID è già stato aggiunto.
       Questo può accadere se il codice non controlla esplicitamente la presenza di un nodo nel grafo prima di aggiungerlo, risultando in nodi
        duplicati per ogni ID che appare in più di una connessione.  Per evitare questo problema e assicurarsi che il numero di nodi nel grafo 
        rifletta correttamente il numero unico di fermate, è importante utilizzare un approccio che impedisca i duplicati, come l'utilizzo di self._idMap
         per mappare gli ID agli oggetti Fermata e aggiungere questi oggetti al grafo, garantendo così che ogni fermata sia rappresentata una sola volta
          nel grafo, indipendentemente dal numero di connessioni in cui appare."""
