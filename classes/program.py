from tkinter import *
from .filterer import Filterer
from .sorterer import Sorterer
from .filemanip import FileManip
from .MenuBuilder import MenuBuilder
class PhotoOrganizer:
	def __init__(self, master, conf):
		master.wm_title("Photo Organizer")
		self.frmTop = Frame(master)
		self.frmTop.pack()
		self.frmBtm = Frame(master)
		self.frmBtm.pack()
		self.mb = MenuBuilder(master)
		self.filt = Filterer(self.frmTop, conf, self.mb.cond)
		self.sort = Sorterer(self.frmBtm, conf)

		master.mainloop()