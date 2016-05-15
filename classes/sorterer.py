from tkinter import *
from .filemanip import FileManip
import os, exifread, re,shutil
from filelock import FileLock
from PIL import PngImagePlugin
from PIL import Image
import enzyme
import logging
class Sorterer:
	def __init__(self, master, config, program):
		self.config = config
		self.fm = FileManip()
		self.program = program
		self.lblNameFormat = Label(master, text="Image Name Format:")
		self.lblNameFormat.grid(row=0, column=0)
		
		self.txtNameFormat = Entry(master, width=22)
		self.txtNameFormat.insert(0, config["ImageNameFormat"])
		self.txtNameFormat.grid(row=1, column=0)
		
		self.lblFolderStructure = Label(master, text="Folder Structure:")
		self.lblFolderStructure.grid(row=0, column=1)
		
		self.txtFolderStructure = Entry(master)
		self.txtFolderStructure.insert(0, config["FolderStructure"])
		self.txtFolderStructure.grid(row=1, column=1)

		self.lblFolderLocation = Label(master, text="Where to Put Structured Images:")
		self.lblFolderLocation.grid(row=2, column=0, columnspan=2)
		
		self.txtFolderLocation = Entry(master, width=44)
		self.txtFolderLocation.insert(0, config["SortFolder"])
		self.txtFolderLocation.grid(row=3, column=0, columnspan=2, sticky=W)
		self.buttonFrame = Frame(master)
		self.buttonFrame.grid(row=4, columnspan=2)
		
		self.btnCopy = Button(self.buttonFrame, text="Copy")
		self.btnCopy.grid(row=0, column=0)

		self.btnMove = Button(self.buttonFrame, text="Move", command=self.structure_images)
		self.btnMove.grid(row=0, column=1)

		self.btnRename = Button(self.buttonFrame, text="Rename", command=self.rename_files)
		self.btnRename.grid(row=0, column=2)

		self.btnRename = Button(self.buttonFrame, text="Rename and Move", command=self.rename_move_images)
		self.btnRename.grid(row=0, column=3)

	def rename_move_images(self):
		self.rename_files()
		self.structure_images()

	def rename_files(self):
		filterFolder = self.program.filt.txtImagesFolder.get()
		if self.fm.check_folder(filterFolder) == -1: return

		fileList = self.fm.get_files(filterFolder)
		countBeforeRename = self.fm.get_file_count(filterFolder)

		for file in fileList:
			nameFormat = self.txtNameFormat.get()
			
			# Find the date and time of the file

			exifDate = self.getExifDate(file)
			# Construct the Image Name Format
			if exifDate != None:
				nameFormat = self.replace_exif_string(nameFormat, exifDate)
			else:
				print("Skipping file '{0}' because no EXIF data was found.".format(file))
				continue
			
			extension     = os.path.splitext(self.fm.get_filename(file))[1]
			fileDirectory = self.fm.get_file_directory(file)
			filePath = os.path.join(fileDirectory,nameFormat)+extension

			
			if not os.path.exists(filePath):
				logging.info("Renaming file '{0}' to {1}".format(file, filePath))
				shutil.move(file, filePath)
			elif filePath == file:
				pass
			else:
				newName = self.fm.correct_collision(filePath)
				logging.info("Renaming file '{0}' to {1}".format(file, newName))
				shutil.move(file, newName)

		countAfterRename = self.fm.get_file_count(filterFolder)
		if countBeforeRename != countAfterRename:
			print("FATAL ERROR. IMAGES DELETED.")
		else:
			print("Renaming Succeeded.")

	def structure_images(self):

		filterFolder = self.program.filt.txtImagesFolder.get()
		if self.fm.check_folder(filterFolder) == -1: return
		
		sortFolder = self.txtFolderLocation.get()
		if self.fm.check_folder(sortFolder) == -1: return

		folderStructureLocation = self.txtFolderStructure.get()
		fileList = self.fm.get_files(filterFolder)
		for file in fileList:
			folderStructure = folderStructureLocation
			exifDate = self.getExifDate(file)
			
			# Construct the Image Name Format
			if exifDate != None:
				folderStructure = self.replace_exif_string(folderStructure, exifDate)
			else:
				print("Skipping file '{0}' because no EXIF data was found.".format(file))
				continue

			filePath = os.path.join(sortFolder, folderStructure, self.fm.get_filename(file))
			
			if not os.path.exists(filePath):
				os.renames(file, filePath)
			elif filePath == file:
				pass
			else:
				os.renames(file, self.fm.correct_collision(filePath))

	def getMOVExifDate(self, path):
		with open(path, 'rb') as f:
			mkv = enzyme.MKV(f)
		return

	def getExifDate(self,path):
		exifDate = None
		if path.lower().endswith("png"):
			exifDate = self.getPNGExifDate(path)
		elif path.lower().endswith("jpg") or path.lower().endswith("jpeg"):
			exifDate = self.getJPGExifDate(path)
		#elif file.lower().endswith("mov"):
		#	exifDate = self.getMOVExifDate(file)
		else:
			#print("Skipping file '{0}' because it is not supported.".format(path))
			return
		return exifDate

	def getPNGExifDate(self, path):
		image = Image.open(path)
		try:
			pngDate = re.findall(r"<photoshop:DateCreated>([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])T([0-9][0-9]):([0-9][0-9]):([0-9][0-9])</photoshop:DateCreated>", image.info["XML:com.adobe.xmp"])
		except KeyError:
			return
		if pngDate == []:
			return
		pngDate = list(pngDate[0])
		pngDate.append("000")
		
		return pngDate


	def getJPGExifDate(self, path):
		exif = open(path, 'rb')
		ex = exifread.process_file(exif, details=False)
		try:
			date = str(ex["EXIF DateTimeOriginal"])
			exifDate = re.findall("([0-9][0-9][0-9][0-9]):([0-9][0-9]):([0-9][0-9]) ([0-9][0-9]):([0-9][0-9]):([0-9][0-9])", date)
			exifDate = list(exifDate[0])
		except KeyError:
			return
		exifDatemillis = object
		try:
			millis = ex["EXIF SubSecTimeOriginal"]
		except KeyError:
			millis = "000"
		try:
			millis = int(str(millis))
		except ValueError:
			millis = "000"

		millisString = ""
		if millis < 10:
			millisString = "00{0}".format(millis)
		elif millis < 100:
			millisString = "0{0}".format(millis)
		else:
			millisString = str(millis)
		exifDate.append(millisString)
		exif.close()
		return exifDate

	def replace_exif_string(self, nameFormat, exifDate):
		nameFormat = nameFormat.replace("YYYY", exifDate[0])
		nameFormat = nameFormat.replace("MM",   exifDate[1])
		nameFormat = nameFormat.replace("DD",   exifDate[2])
		nameFormat = nameFormat.replace("hh",   exifDate[3])
		nameFormat = nameFormat.replace("mm",   exifDate[4])
		nameFormat = nameFormat.replace("ss",   exifDate[5])
		nameFormat = nameFormat.replace("uuu",  exifDate[6])
		return nameFormat


