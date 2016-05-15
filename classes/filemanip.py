import ntpath, os,shutil
from tkinter import *
from tkinter import messagebox
class FileManip:
	def get_files(self, path):
		"""Returns all files in the directory 'path'."""
		fileList = []
		for root, dirs, files in os.walk(path):
			for f in os.listdir(root):
				if os.path.isfile(os.path.join(root,f)):
					fileList.append(os.path.join(root,f))
		return fileList

	def get_filename(self, path):
		path, name = ntpath.split(path)
		return name

	def get_file_directory(self, path):
		path, name = ntpath.split(path)
		return path

	def get_file_count(self, path):
		if not os.path.exists(path):
			return -1
		return len(self.get_files(path))

	def copy_file(self, filePath, directory):
			if not os.path.exists(os.path.join(directory, get_filename(filePath))):
				shutil.copy(filePath, directory)
			else:
				print("The file '{0}' already exists in the destination folder".format(filePath))

	def move_file(self, filePath, directory):
			if not os.path.exists(os.path.join(directory, self.get_filename(filePath))):
				shutil.move(filePath, directory)
			else:
				print("The file '{0}' already exists in the destination folder".format(filePath))

	def correct_collision(self, path):
		extension     = os.path.splitext(self.get_filename(path))[1]
		fileName      = os.path.splitext(self.get_filename(path))[0]
		testFileName  = fileName
		fileDirectory = self.get_file_directory(path)
		fileNumber    = 0

		while os.path.exists(os.path.join(fileDirectory,testFileName)+extension):
			fileNumber += 1
			testFileName = "{0}-{1}".format(fileName, str(fileNumber))

		return os.path.join(fileDirectory,testFileName)+extension

	def check_folder(self, path):
		if not os.path.exists(path):
			messagebox.showwarning("Warning", "The folder '{0}' does not exist. Please select another folder.".format(path))
			return -1