import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._choiceAeroportoA = None
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._choiceAeroportoP = None

    def handleAnalizza(self, e):
        x = self._view._txtInNumC.value
        try:
            int(x)
        except ValueError:
            self._view.create_alert("Inserire un numero intero")
            self._view.update_page()
            return

        self._model.buildgraph(int(x))

        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. "))
        self._view._txt_result.controls.append(
            ft.Text(f"Num nodi: {self._model.get_num_of_nodes()}"))
        self._view._txt_result.controls.append(
            ft.Text(f"Num archi: {self._model.get_num_of_edges()}"))
        self._view._ddAeroportoP.disabled = False
        self._view._ddAeroportoA.disabled = False
        self._view._btnConnessi.disabled = False
        self._view._btnPercorso.disabled = False
        self._view._txtInNumTratte.disabled = False
        self._view._btnCercaItinerario.disabled = False
        self.fillDD()
        self._view.update_page()

    def handleConnessi(self, e):

        a1 = self._choiceAeroportoP

        result = self._model.getSortedNeighbors(a1)
        for node in result:
            self._view._txt_result.controls.append(ft.Text(
                f"{node[0]}, voli: {node[1]}"))

        self._view.update_page()

    def handleTestConnessione(self, e):

        a1 = self._choiceAeroportoP
        a2 = self._choiceAeroportoA

        boolean = self._model.verificaConnesione(a1,a2)

        if boolean == True:
            self._view._txt_result.controls.append(ft.Text("Esiste collegamento"))
        else:
            self._view._txt_result.controls.append(ft.Text("Non esiste collegamento"))

        self._view.update_page()


    def handleCercaItinerario(self, e):

        a1 = self._choiceAeroportoP
        a2 = self._choiceAeroportoA
        t = int(self._view._txtInNumTratte.value)

        self._model.calcPath(a1, a2, t)

        percorso = self._model.solBest

        for i in range(0, len(percorso)-1):
            self._view._txt_result.controls.append(ft.Text(
                f"{percorso[i]} -> {percorso[i+1]}"))

        self._view.update_page()

    def fillDD(self):

        listaAeroporti = self._model.get_nodes()

        for node in listaAeroporti:
            self._view._ddAeroportoP.options.append(ft.dropdown.Option(data=node, on_click=self.readDDAeroportoP, text=node.AIRPORT))
            self._view._ddAeroportoA.options.append(ft.dropdown.Option(data=node, on_click=self.readDDAeroportoA, text=node.AIRPORT))


    def readDDAeroportoP(self, e):
        if e.control.data is None:
            self._choiceAeroportoP = None
        else:
            self._choiceAeroportoP = e.control.data

    def readDDAeroportoA(self, e):
        if e.control.data is None:
            self._choiceAeroportoA = None
        else:
            self._choiceAeroportoA = e.control.data