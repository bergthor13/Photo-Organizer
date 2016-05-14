from tkinter import *
class Sorterer:
	def __init__(self, master, config):
		self.lblNameFormat = Label(master, text="Image Name Format")
		self.lblNameFormat.grid(row=0, column=0)
		
		self.txtNameFormat = Entry(master)
		self.txtNameFormat.insert(0, config["ImageNameFormat"])
		self.txtNameFormat.grid(row=1, column=0)
		
		self.lblFolderStructure = Label(master, text="Folder Structure")
		self.lblFolderStructure.grid(row=0, column=1)
		
		self.txtFolderStructure = Entry(master)
		self.txtFolderStructure.insert(0, config["FolderStructure"])
		self.txtFolderStructure.grid(row=1, column=1)

		self.lblFolderLocation = Label(master, text="Location of Folder")
		self.lblFolderLocation.grid(row=2, column=0, columnspan=2)
		
		self.txtFolderLocation = Entry(master, width=42)
		self.txtFolderLocation.insert(0, config["SortFolder"])
		self.txtFolderLocation.grid(row=3, column=0, columnspan=2, sticky=W)

		self.btnCopy = Button(master, text="Copy")
		self.btnCopy.grid(row=1, column=2)

		self.btnMove = Button(master, text="Move")
		self.btnMove.grid(row=2, column=2)

		self.btnRename = Button(master, text="Rename")
		self.btnRename.grid(row=3, column=2)