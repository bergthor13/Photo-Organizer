from tkinter import *
from .filterer import Filterer
from .sorterer import Sorterer
from .filemanip import FileManip
from .MenuBuilder import MenuBuilder
import json, os
import atexit
class PhotoOrganizer:
	def __init__(self, master):
		self.master = master
		# Load the configuration file.
		if os.path.exists("config.json"):
			with open('config.json', 'r') as file:
				self.conf = json.loads(file.read())
		else:
			self.conf = {}
			self.conf["FilterFolder"]   = ""
			self.conf["FilteredFolder"] = ""
			self.conf["SortFolder"]     = ""

			self.conf["ImageNameFormat"] = ""
			self.conf["FolderStructure"] = ""

		master.wm_title("Photo Organizer")
		# Will only save data when window is closed manually.
		# Not CMD/CTRL-Q
		master.protocol("WM_DELETE_WINDOW", self.close_window)
		

		self.frmTop = Frame(master)
		self.frmTop.pack()
		self.frmBtm = Frame(master)
		self.frmBtm.pack()
		self.mb = MenuBuilder(master)
		self.filt = Filterer(self.frmTop, self.conf, self)
		self.sort = Sorterer(self.frmBtm, self.conf, self)
		
		master.mainloop()

	def close_window(self):
		self.conf["FilterFolder"]   = self.filt.txtImagesFolder.get()
		self.conf["FilteredFolder"] = self.filt.txtFilteredFolder.get()
		self.conf["SortFolder"]     = self.sort.txtFolderLocation.get()

		self.conf["ImageNameFormat"] = self.sort.txtNameFormat.get()
		self.conf["FolderStructure"] = self.sort.txtFolderStructure.get()
		
		with open('config.json', 'w') as outfile:
			json.dump(self.conf, outfile)
		self.master.destroy()