from tkinter import *
from tkinter import messagebox
import os, exifread,shutil
from .filemanip import FileManip
import logging
class Filterer:
	def __init__(self, master, config, program):
		self.editors = {}
		self.fileList = []
		self.program = program
		self.conditions = program.mb.cond
		self.fm = FileManip()
		self.filter_screens = IntVar()
		self.lblImagesFolder = Label(master, text="Images to Filter and/or Organize:")
		self.lblImagesFolder.grid(row=0, column=0, columnspan=2)
		
		self.txtImagesFolder = Entry(master, width=44)
		self.txtImagesFolder.insert(0, config["FilterFolder"])
		self.txtImagesFolder.grid(row=1, column=0, columnspan=2)
		
		self.lblFilteredFolder = Label(master, text="Where Filtered Images Go:")
		self.lblFilteredFolder.grid(row=2, column=0, columnspan=2)
		
		self.txtFilteredFolder = Entry(master, width=44)
		self.txtFilteredFolder.insert(0, config["FilteredFolder"])
		self.txtFilteredFolder.grid(row=3, column=0, columnspan=2)

		self.lblImagesFolder = Label(master, text="Filter based on conditions window.")
		self.lblImagesFolder.grid(row=6, column=0, columnspan=2)

		self.btnFilter = Button(master, text="Filter", command=self.filter_images)
		self.btnFilter.grid(row=8, column=0, columnspan=2)


	def filter_images(self):
		if self.program.mb.cond.windowOpen == True:
			messagebox.showinfo("Information", "Please close the Conditions window.")
			return

		imageFolder = self.txtImagesFolder.get()
		if self.fm.check_folder(imageFolder) == -1: return

		destDirectory = self.txtFilteredFolder.get()
		if self.fm.check_folder(destDirectory) == -1: return

		images = self.fm.get_files(imageFolder)
		for cond in self.conditions.get_conditions():
			if cond[0] == "EXIF Tag Name":
				images = self.filter_by_exif_tag(cond[1], cond[2], images, cond[3])
			elif cond[0] == "File Extension":
				images = self.filter_by_extension(cond[1], cond[2], images)
			elif cond[0] == "File Name":
				images = self.filter_by_name(cond[1], cond[2], images)

		if len(images) == 0:
			messagebox.showinfo("Information", "There are no images to move.\nPlease refine your filters in\nOptions->Conditions")
		else:
			if messagebox.askyesno("Move", "{0} images will be moved to the destination folder.\nDo you wish to proceed?".format(len(images))):
				for image in images:
					newFilePath = os.path.join(destDirectory,self.fm.get_filename(image))
					if not os.path.exists(newFilePath):
						logging.info("Renaming file '{0}' to {1}".format(image, newFilePath))
						shutil.move(image, newFilePath)
					elif newFilePath == image:
						pass
					else:
						newName = self.fm.correct_collision(newFilePath)
						logging.info("Renaming file '{0}' to {1}".format(image, newName))
						shutil.move(image, newName)


	def filter_by_exif_tag(self, condition, userInput, lis, exifTag):
		res = []
		for file in lis:
			exif = open(file, 'rb')
			try:
				ex = exifread.process_file(exif)
				software = ex[exifTag]
				if self.compare_string(condition, userInput, str(software)):
					res.append(file)
			except KeyError:
				pass
			finally:
				exif.close()
		return res

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
			return string.startswith(userInput)
		if condition == "Ends With":
			return string.endswith(userInput)
		if condition == "Contains":
			return userInput in string
		if condition == "Equals":
			return userInput == string