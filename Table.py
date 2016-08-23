import Tkinter as tk
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel

class VisualTable(tk.Frame):
    def __init__(self, master=None, data=None):
        tk.Frame.__init__(self, master)
        #########################################
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.grid(sticky=tk.NW+tk.SE)
        #########################################
        self.F = tk.Frame(self)
        self.F.grid(row=0, column=0, sticky=tk.NW+tk.SE)
        self.createWidgets(data)

    def createWidgets(self, data):
        if data:
            model = TableModel()
            model.importDict(data)
            self.table = TableCanvas(self.F, model=model)
        else:
            self.table = TableCanvas(self.F)
        self.table.createTableFrame()
