import tkinter
import tkinter.filedialog
import tkinter.messagebox

import os
import shutil
import re


class Window(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.replayDir = os.getenv("LOCALAPPDATA") + "\TslGame\Saved\Demos"
        self.init_window()

    def init_window(self):

        self.master.title("Replay Manager PUBG")
        self.master.state('zoomed')
        self.pack(fill=tkinter.BOTH, expand=1)

        tkinter.Button(self, text="Open folder", command=self.openFolder).pack()
        tkinter.Button(self, text="Import", command=self.importReplay).pack()

        menu = tkinter.Menu(self.master)
        self.master.config(menu=menu)

        file = tkinter.Menu(menu)
        file.add_command(label="Open folder", command=self.openFolder)
        file.add_command(label="Import replay", command=self.importReplay)
        menu.add_cascade(label="File", menu=file)

        # edit = tkinter.Menu(menu)
        # edit.add_command(label="Undo")
        # menu.add_cascade(label="Edit", menu=edit)

    def openFolder(self):
        if not os.path.isdir(self.replayDir):
            tkinter.messagebox.showerror("Folder doesn't exist", "The replays folder doesn't exist!")
            return 
        os.system("start /max {}".format(self.replayDir))

    def importReplay(self):
        folder = tkinter.filedialog.askdirectory()

        if not folder:
            return

        folderName = folder.split("/")[-1]

        if os.path.isdir(self.replayDir + "/" + folderName):
            tkinter.messagebox.showerror("Already exists", "The replay already exists!")
            return

        match = re.findall(r"(match\.bro\.official\.\d{4}-\d{2}\.(us|eu|as|uc)\."
                           r"(solo|duo|squad)\.\d{4}\.\d{2}\.\d{2}\.[a-z0-9-]*?__USER__\d+)", folderName)

        def notValid():
            tkinter.messagebox.showerror("Invalid folder", "Not valid folder name!")

        if len(match) != 1:
            notValid()
            return

        if match[0][0] != folderName:
            notValid()
            return

        # TODO More tests

        shutil.copytree(folder, self.replayDir + "/" + folderName)


root = tkinter.Tk()
app = Window(root)
root.mainloop()
