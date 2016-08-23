from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog, tkMessageBox
import os
import csv
import networkx as nx
from Table import *

class VisualNetx(object):
    def __init__(self):
        self.parent = Tk()
        self.menu_bar = Menu(self.parent)

    def setTitle(self, title):
        self.parent.title(title)

    def start(self):
        self.parent.mainloop()

    def sayHello(self, event=None):
        print "hello"

    def openFile(self):
        filename=tkFileDialog.askopenfile(defaultextension='.csv',
                                            filetypes=[("Data file","*.csv"),
                                                       ("All files","*.*")],
                                            title='Choose data from a .csv file saved as excel spreadsheet in .csv format (comma separated list)',
                                            parent=self.parent)
        if filename and os.path.exists(filename.name) and os.path.isfile(filename.name):
            datafile = filename.name
        return datafile

    def loadTable(self, event=None):
        # open up a dialog and load the csv data
        dataLst, dataTable, columns = [], {}, []
        #try:
        filename = self.openFile()
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            dataLst, dataTable = [], {}
            data = list(reader)
            columns = data[0]
            for i in xrange(1, len(data)):
                dataLst.append(data[i])
                dataTable[i] = {}
                for j in xrange(len(columns)):
                    dataTable[i][columns[j]] = data[i][j]
        table = VisualTable(data=dataTable)
        '''except:
            print("Unexpected error:", sys.exc_info()[0])
            tkMessageBox.showwarning(
                "Open file",
                "Cannot open this file\n(%s)" % filename
            )
            return'''


    def initMenus(self):
        file_menu = Menu(self.menu_bar, tearoff=0)
        edit_menu = Menu(self.menu_bar, tearoff=0)
        view_menu = Menu(self.menu_bar, tearoff=0)
        about_menu = Menu(self.menu_bar, tearoff=0)

        # add file edit dropdown menus
        file_menu.add_command(label="New", underline=0, accelerator='Command+N', command=self.sayHello)
        file_menu.add_command(label="Open", underline=0, accelerator='Command+O',command=self.loadTable)
        file_menu.add_command(label="Save", underline=0, accelerator='Command+s', command=self.sayHello)
        file_menu.add_command(label="Save as", underline=0, accelerator='Shift+Command+s', command=self.sayHello)
        file_menu.add_command(label="Close", underline=0, accelerator='Command+W', command=self.sayHello)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", underline=0, accelerator='Command+Q', command=self.parent.quit)

        # bind event to parent panel, ignore cases
        self.parent.bind('<Command-n>', self.sayHello)
        self.parent.bind('<Command-N>', self.sayHello)
        self.parent.bind('<Command-o>', self.loadTable)
        self.parent.bind('<Command-O>', self.loadTable)
        self.parent.bind('<Command-s>', self.sayHello)
        self.parent.bind('<Command-S>', self.sayHello)
        self.parent.bind('<Shift-Command-s>', self.sayHello)
        self.parent.bind('<Shift-Command-S>', self.sayHello)
        self.parent.bind('<Command-w>', self.sayHello)
        self.parent.bind('<Command-W>', self.sayHello)

        edit_menu.add_command(label="Copy", underline=0, accelerator='Command+C', command=self.sayHello)
        edit_menu.add_command(label="Cut", underline=0, accelerator='Command+X', command=self.sayHello)
        edit_menu.add_command(label="Paste", underline=0, accelerator='Command+V', command=self.sayHello)
        edit_menu.add_command(label="Undo", underline=0, accelerator='Command+Z', command=self.sayHello)
        edit_menu.add_command(label="Select All", underline=0, accelerator='Command+A', command=self.sayHello)

        #add menus to menu bar
        self.menu_bar.add_cascade(label='File', menu=file_menu)
        self.menu_bar.add_cascade(label='Edit', menu=edit_menu)
        self.menu_bar.add_cascade(label='View', menu=view_menu)
        self.menu_bar.add_cascade(label='About', menu=about_menu)

        self.parent.config(menu=self.menu_bar)


if __name__ == "__main__":
    vn = VisualNetx()
    vn.setTitle('Social Network Visualization and Analysis')
    vn.initMenus()
    vn.start()
