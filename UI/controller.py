import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # the controller
        self._fermataArrivo = None
        self._fermataPartenza = None

    def handleCreaGrafo(self, e):
        self._model.buildGraph()
        numNodes = self._model.getNodesNumber()
        numEdges = self._model.getEdgesNumber()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.lst_result.controls.append(ft.Text(f"Numero di nodi: {numNodes}"))
        self._view.lst_result.controls.append(ft.Text(f"Numero di archi: {numEdges}"))
        self._view._btnCalcola.disabled = False
        self._view.update_page()

    def handleCreaGrafoPesato(self, e):
        self._model.buildGraphPesato()
        numNodes = self._model.getNodesNumber()
        numEdges = self._model.getEdgesNumber()
        archi_peso_maggiore = self._model.getArchiPesoMaggiore()
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo creato correttamente!"))
        self._view.lst_result.controls.append(ft.Text(f"Numero di nodi: {numNodes}"))
        self._view.lst_result.controls.append(ft.Text(f"Numero di archi: {numEdges}"))
        self._view.lst_result.controls.append(ft.Text("Archi con peso maggiore:"))
        for arco in archi_peso_maggiore:
            self._view.lst_result.controls.append(
                ft.Text(f"partenza da: {arco[0]} --> arrivo a: {arco[1]} con Peso: {arco[2]}"))
        self._view._btnCalcola.disabled = False
        self._view._btnCalcolaPercorso.disabled = False
        self._view._btnCalcolaPercorsoECosto.disabled = False
        self._view.update_page()

    def handleCercaRaggiungibili(self, e):
        if self._fermataPartenza is None:
            # Mostra un messaggio di errore o semplicemente non eseguire alcuna azione
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Seleziona una stazione di partenza."))
            self._view.update_page()
            return  # Interrompe l'esecuzione se non è stata selezionata una fermata di partenza

        raggiunti = self._model.cercaRaggiungibili_DFS(self._fermataPartenza)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Fermate raggiungibili:"))
        for v in raggiunti:
            self._view.lst_result.controls.append(ft.Text(f"{v.nome}"))
        self._view.update_page()

    def loadFermate(self, dd: ft.Dropdown()):
        fermate = self._model.fermate

        if dd.label == "Stazione di Partenza":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Partenza))
        elif dd.label == "Stazione di Arrivo":
            for f in fermate:
                dd.options.append(ft.dropdown.Option(text=f.nome,
                                                     data=f,
                                                     on_click=self.read_DD_Arrivo))

    def read_DD_Partenza(self, e):
        print("read_DD_Partenza called ")
        if e.control.data is None or e.control.data == "":
            self._fermataPartenza = None
        else:
            self._fermataPartenza = e.control.data

    def read_DD_Arrivo(self, e):
        print("read_DD_Arrivo called ")
        if e.control.data is None:
            self._fermataArrivo = None
        else:
            self._fermataArrivo = e.control.data

    # Cammini minimi
    def handlePercorso(self, e):
        if self._fermataPartenza is None or self._fermataArrivo is None:
            # Mostra un messaggio di errore o semplicemente non eseguire alcuna azione
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Seleziona una stazione di partenza e di arrivo."))
            self._view.update_page()
            return
        path = self._model.getBestPath(self._fermataPartenza, self._fermataArrivo)
        if path is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Non esiste un percorso tra le due fermate selezionate."))
            self._view.update_page()
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Percorso migliore:"))
        for v in path:
            self._view.lst_result.controls.append(ft.Text(f"{v.nome}"))
        self._view.update_page()

    def handlePercorsoECosto(self, e):
        if self._fermataPartenza is None or self._fermataArrivo is None:
            # Mostra un messaggio di errore o semplicemente non eseguire alcuna azione
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Seleziona una stazione di partenza e di arrivo."))
            self._view.update_page()
            return
        totTime, path = self._model.getBestPathAndCost(self._fermataPartenza, self._fermataArrivo)
        if path is None:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Non esiste un percorso tra le due fermate selezionate."))
            self._view.update_page()
            return
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Percorso trovato!"))
        self._view.lst_result.controls.append(ft.Text(f"Il cammino più breve fra "
                                                      f"{self._fermataPartenza} e "
                                                      f"{self._fermataArrivo} impiega "
                                                      f"{totTime} minuti."))
        for fermata in path:
            self._view.lst_result.controls.append(ft.Text(f"{fermata}"))
        self._view.update_page()

