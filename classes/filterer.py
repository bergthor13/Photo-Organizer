from tkinter import *
import os, exifread
from .filemanip import FileManip
class Filterer:
	def __init__(self, master, config):
		self.editors = {}
		self.fileList = []
		self.fm = FileManip()
		self.filter_screens = IntVar()
		self.lblImagesFolder = Label(master, text="Images to Filter:")
		self.lblImagesFolder.grid(row=0, column=0, columnspan=2)
		
		self.txtImagesFolder = Entry(master, width=42)
		self.txtImagesFolder.insert(0, config["FilterFolder"])
		self.txtImagesFolder.grid(row=1, column=0, columnspan=2)
		
		self.lblFilteredFolder = Label(master, text="Filtered Images:")
		self.lblFilteredFolder.grid(row=2, column=0, columnspan=2)
		
		self.txtFilteredFolder = Entry(master, width=42)
		self.txtFilteredFolder.insert(0, config["FilteredFolder"])
		self.txtFilteredFolder.grid(row=3, column=0, columnspan=2)


		
		self.lblEditors = Label(master, text="Values:")
		self.lblEditors.grid(row=0, column=2)
		self.Lb1 = Listbox(master, selectmode=MULTIPLE)
		self.Lb1.grid(row=1, column=2, rowspan=8)

		self.btnSE = Button(master, text="Find Software Editors", command=self.find_software_editors)
		self.btnSE.grid(row=9, column=2)

		self.lblImagesFolder = Label(master, text="Filter based on conditions")
		self.lblImagesFolder.grid(row=6, column=0, columnspan=2)

		self.btnFilter = Button(master, text="Filter", command=self.filter_images)
		self.btnFilter.grid(row=8, column=0, columnspan=2)



	def find_software_editors(self):
		self.fileList = self.fm.get_files(self.txtImagesFolder.get())
		self.Lb1.delete(0, len(self.editors)-1)
		self.editors = {}
		
		if not os.path.exists(self.txtFilteredFolder.get()):
			return
		if not os.path.exists(self.txtImagesFolder.get()):
			return

		for file in self.fileList:
			exif = open(file, 'rb')
			try:
				ex = exifread.process_file(exif)
				software = ex["Image Software"]
				
				if not str(software) in self.editors:
					self.editors[str(software)] = []
					self.Lb1.insert(len(self.editors),str(software))
				self.editors[str(software)].append(file)

			except KeyError:
				pass#print("No editor for image '{0}'".format(f))


	def filter_screen_shot(self):
		if not os.path.exists(self.txtFilteredFolder.get()):
			return
		if not os.path.exists(self.txtImagesFolder.get()):
			return

		currFolder = os.path.join(self.txtFilteredFolder.get(), "Screen Shots")
		if not os.path.exists(currFolder):
			os.mkdir(currFolder)

		screenShots = [x for x in self.fm.get_files(self.txtImagesFolder.get()) if x.lower().endswith(".png")]
		for file in screenShots:
			self.fm.move_file(file, currFolder)
		print("Done")


	def filter_images(self):
		if not os.path.exists(self.txtFilteredFolder.get()):
			return
		if not os.path.exists(self.txtImagesFolder.get()):
			return

		for li in self.Lb1.curselection():
			
			currEditor = self.Lb1.get(li)
			if not os.path.exists(self.txtFilteredFolder.get()):
				return
			currFolder = os.path.join(self.txtFilteredFolder.get(), currEditor)
			
			print("Filtering {0}...".format(currEditor))

			if not os.path.exists(currFolder):
				os.mkdir(currFolder)
			
			for f in self.editors[currEditor]:
				self.fm.move_file(f, currFolder)
			print("Done")

		if self.filter_screens.get() == 1:
			self.filter_screen_shot()