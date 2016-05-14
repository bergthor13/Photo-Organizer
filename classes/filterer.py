from tkinter import *
import os, exifread
from .filemanip import FileManip
class Filterer:
	def __init__(self, master, config, conditions):
		self.editors = {}
		self.fileList = []
		self.conditions = conditions
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

		self.btnSE = Button(master, text="Find Software Editors", command=None)
		self.btnSE.grid(row=9, column=2)

		self.lblImagesFolder = Label(master, text="Filter based on conditions")
		self.lblImagesFolder.grid(row=6, column=0, columnspan=2)

		self.btnFilter = Button(master, text="Filter", command=self.filter_images)
		self.btnFilter.grid(row=8, column=0, columnspan=2)

	def filter_images(self):
		print("Calling Conditions")
		images = self.fm.get_files(self.txtImagesFolder.get())
		for cond in self.conditions.get_conditions():
			
			if cond[0] == "Exif Tag Name":
				images = self.filter_by_exif_tag(cond[1], cond[2], images)
			elif cond[0] == "File Extension":
				images = self.filter_by_extension(cond[1], cond[2], images)
			elif cond[0] == "File Name":
				images = self.filter_by_name(cond[1], cond[2], images)
		print("FINAL RESULT")
		print(images)
		return images


	def filter_by_exif_tag(self, condition, userInput, lis):
		return lis
	def filter_by_name(self, condition, userInput, lis):
		res = []
		for file in lis:
			# Get the file name
			fileName = os.path.splitext(self.fm.get_filename(file))[0]
			
			if self.compare_string(condition, userInput, fileName):
				res.append(file)
		return res

	def filter_by_extension(self, condition, userInput, lis):
		res = []
		for file in lis:
			# Get the file name
			fileExtension = os.path.splitext(self.fm.get_filename(file))[1][1:]
			if self.compare_string(condition, userInput.lower(), fileExtension.lower()):
				res.append(file)
		return res






	def compare_string(self, condition, userInput, string):
		if condition == "Begins With":
			print(string, userInput)
			return string.startswith(userInput)
		if condition == "Ends With":
			return string.endswith(userInput)
		if condition == "Contains":
			return userInput in string
		if condition == "Equals":
			return userInput == string