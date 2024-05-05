import flet as ft
import os


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Metro Paris"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = 1200  # window's width is 200 px
        page.window_height = 800
        page.window_center()
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self.__theme_switch = None
        self.lst_result = None
        self._title = None
        self._logo = None
        self._ddStazArrivo = None
        self._ddStazPartenza = None
        self._btnCrea = None
        self._btnCalcola = None
        self._btnCalcolaPercorso = None
        self._btnCalcolaPercorsoECosto = None

    def load_interface(self):
        # title
        self.__theme_switch = ft.Switch(label="Dark Theme", on_change=self.theme_changed)
        self._title = ft.Text("Metro Paris", color="green", size=24)

        # ROW with title
        img_path = os.path.join(os.getcwd(), 'database/RATP.png')
        self._logo = ft.Image(src=img_path,
                              width=100,
                              height=100,
                              )
        row0 = ft.Row([self.__theme_switch], alignment=ft.MainAxisAlignment.START)
        row1 = ft.Row([self._title, self._logo],
                      alignment=ft.MainAxisAlignment.CENTER)

        # Row with controls
        self._btnCrea = ft.ElevatedButton(text="Crea Grafo", on_click=self._controller.handleCreaGrafoPesato, )
        self._ddStazPartenza = ft.Dropdown(label="Stazione di Partenza")
        self._ddStazArrivo = ft.Dropdown(label="Stazione di Arrivo")
        self._btnCalcola = ft.ElevatedButton(text="Calcola Raggiungibili",
                                             on_click=self._controller.handleCercaRaggiungibili,
                                             disabled=True)
        self._btnCalcolaPercorso = ft.ElevatedButton(text="Calcola Percorso",
                                                     on_click=self._controller.handlePercorso,
                                                     disabled=True)
        self._btnCalcolaPercorsoECosto = ft.ElevatedButton(text="Calcola Percorso e Costo",
                                                           on_click=self._controller.handlePercorsoECosto,
                                                           disabled=True)
        # Load elements in DD
        self._controller.loadFermate(self._ddStazPartenza)
        self._controller.loadFermate(self._ddStazArrivo)

        row2 = ft.Row([self._btnCrea,
                       self._ddStazPartenza,
                       self._ddStazArrivo,
                       self._btnCalcola,
                       self._btnCalcolaPercorso,
                       ], alignment=ft.MainAxisAlignment.CENTER, spacing=30)
        row3 = ft.Row([self._btnCalcolaPercorsoECosto], alignment=ft.MainAxisAlignment.CENTER)

        # Row with listview
        self.lst_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=False)

        self._page.add(row0, row1, row2, row3, self.lst_result)

        self._page.update()

    def set_controller(self, controller):
        self._controller = controller

    def theme_changed(self, e):
        """Function that changes the color theme of the app, when the corresponding
        switch is triggered"""
        self._page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self._page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.__theme_switch.label = (
            "Light theme" if self._page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        self.update_page()

    def update_page(self):
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller
