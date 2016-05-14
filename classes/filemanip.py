import ntpath, os
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