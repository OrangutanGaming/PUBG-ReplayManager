import tkinter
import tkinter.filedialog
import tkinter.messagebox

import os
import shutil
import re
import zipfile


class Window(tkinter.Frame):

    def __init__(self, master=None):
        tkinter.Frame.__init__(self, master)
        self.master = master
        self.replayDir = os.getenv("LOCALAPPDATA") + "\TslGame\Saved\Demos"
        self.tempDir = os.getenv("TEMP")
        self.init_window()

    def init_window(self):

        self.master.title("Replay Manager PUBG")
        self.master.state("zoomed")
        self.pack(fill=tkinter.BOTH, expand=1)

        tkinter.Button(self, text="Open folder", command=self.openFolder).pack()

        menu = tkinter.Menu(self.master)
        self.master.config(menu=menu)

        file = tkinter.Menu(menu, tearoff=False)
        file.add_command(label="Open folder", command=self.openFolder)
        menu.add_cascade(label="File", menu=file)
        importMenu = tkinter.Menu(file, tearoff=False)
        importMenu.add_command(label="Import Folder", command=self.importReplayFolder)
        importMenu.add_command(label="Import Archive", command=self.importReplayZip)
        file.add_cascade(label="Import", menu=importMenu)

    def openFolder(self):
        if not os.path.isdir(self.replayDir):
            tkinter.messagebox.showerror("Folder doesn't exist", "The replays folder doesn't exist!")
            return 
        os.system("start /max {}".format(self.replayDir))

    def importReplayFolder(self):
        folder = tkinter.filedialog.askdirectory()
        self.importReplay(folder)

    def importReplayZip(self):
        archives = tkinter.filedialog.askopenfilenames(defaultextension=".zip",
                                                      filetypes=[("Archive", "*.zip")])

        for archive in archives:
            archiveName = archive.split("/")[-1]

            if not archive.endswith((".zip")):
                return

            archiveName = archiveName.strip(".zip")

            if os.path.isdir(self.tempDir + "/" + archiveName):
                shutil.rmtree(self.tempDir + "/" + archiveName)

            with zipfile.ZipFile(archive) as archiveF:
                archiveF.extractall(self.tempDir + "/" + archiveName)

            self.importReplay(self.tempDir + "/" + archiveName)

    def importReplay(self, folderPath):

        if not folderPath:
            return

        folderName = folderPath.split("/")[-1]

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

        shutil.copytree(folderPath, self.replayDir + "/" + folderName)


root = tkinter.Tk()
app = Window(root)
root.mainloop()
