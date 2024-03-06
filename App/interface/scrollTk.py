import tkinter as tk

"""
    Permet d'initialiser une fenêtre incluant une scroll bar
    Toutes les méthodes commencent par "scroll" pour éviter de faire des surcharges involontaire

    Source: http://stackoverflow.com/a/3092341
"""
class scrollTk(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        self._scrollCanvas = tk.Canvas(self, width=1220, height=800)
        self._scrollCanvas.pack(side=tk.LEFT, fill="both", expand=True)

        scrollbar = tk.Scrollbar(self, command=self._scrollCanvas.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')

        self._scrollCanvas.configure(yscrollcommand = scrollbar.set)

        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self._scrollCanvas.bind('<Configure>', self.__scrollOnConfigure)

        self._scrollFrame = tk.Frame(self._scrollCanvas)
        self._scrollCanvas.create_window((0,0), window=self._scrollFrame, anchor='nw')

    def __scrollOnConfigure(self, event):
        self.updateScroll()

    def updateScroll(self):
        self._scrollCanvas.configure(scrollregion=self._scrollCanvas.bbox('all'))

    def getMainFrame(self):
        return self._scrollFrame
