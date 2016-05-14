from tkinter import *
from .conditions import Conditions
class MenuBuilder:
	def __init__(self, master):
		self.master = master
		self.cond = Conditions(master)
		menu = Menu(self.master)
		master.config(menu=menu)
		optionsMenu = Menu(menu)
		menu.add_cascade(label="Options", menu=optionsMenu)
		optionsMenu.add_command(label="Conditions", command=self.cond.display)