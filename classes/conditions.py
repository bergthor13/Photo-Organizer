from tkinter import *
class Conditions:
	def __init__(self, master):
		self.master = master
		self.conOptions = [
			"EXIF Tag Name",
			"File Extension",
			"File Name",
		]
		self.conConditions = [
			"Begins With",
			"Ends With",
			"Contains",
			"Equals",
		]
		self.values = []
		self.widgets = []

	def display(self):
		self.window = Toplevel(self.master)
		self.window.wm_title("Conditions")
		self.window.protocol("WM_DELETE_WINDOW", self.close_window)
		if len(self.values) == 0:
			self.add_condition()
		else:
			for i, c in enumerate(self.values):
				self.displayRow(i+1, c, self.widgets[i])
		Label(self.window, text="Select the conditions for the files to be excluded").grid(row=0, column=0, columnspan=4)
		self.btnAdd = Button(self.window, text="+", command=self.add_condition)
		self.btnAdd.grid(row=0, column=4)
		self.btnRemove = Button(self.window, text="Clear", command=self.clear_conditions)
		self.btnRemove.grid(row=0, column=5)


	def displayRow(self, index, values, widgets):
		if values[0].get() == "EXIF Tag Name":
			widgets[0] = OptionMenu(self.window, values[0], *self.conOptions)
			widgets[0].grid(row=index, column=0)
			
			widgets[2] = Entry(self.window, width=20)
			widgets[2].insert(0, values[3])
			widgets[2].grid(row=index, column=1)
			widgets[1] = OptionMenu(self.window, values[1], *self.conConditions)
			widgets[1].grid(row=index, column=2)
			
			widgets[3] = Entry(self.window, width=19)
			widgets[3].insert(0, values[2])
			widgets[3].grid(row=index, column=3)
		else:
			widgets[0] = OptionMenu(self.window, values[0], *self.conOptions)
			widgets[0].grid(row=index, column=0)
			widgets[1] = OptionMenu(self.window, values[1], *self.conConditions)
			widgets[1].grid(row=index, column=1)
			widgets[2] = Entry(self.window, width=42)
			widgets[2].insert(0, values[2])
			widgets[2].grid(row=index, column=2, columnspan=2)

	def add_condition(self):
		newOptOption = StringVar()
		newOptOption.set("EXIF Tag Name")
		newOptOption.trace("w", self.refresh_conditions)
		newOptCondit = StringVar()
		newOptCondit.set("Begins With")
		newOptCondit.trace("w", self.refresh_conditions)
		newCondition = [newOptOption,newOptCondit, "", ""]
		newCondWidget = [None, None, None, None]
		self.values.append(newCondition)
		self.widgets.append(newCondWidget)
		self.displayRow(len(self.values), newCondition, newCondWidget)
		self.save_changes()
		self.refresh_conditions()

	def clear_conditions(self):
		for c in self.widgets:
			for w in c:
				w.destroy()
		self.values = []
		self.widgets = []
		self.add_condition()

	def refresh_conditions(self, *args):
		for i, c in enumerate(self.widgets):
			for w in c:
				w.destroy()
			self.displayRow(i+1, self.values[i], self.widgets[i])

	def save_changes(self):
		for i, w in enumerate(self.widgets):
			if self.values[i][0].get() == "EXIF Tag Name":
				if w[3] != None:
					self.values[i][3] = w[2].get()
				if w[2] != None:
					self.values[i][2] = w[3].get()
			else:
				if w[2] != None:
					self.values[i][2] = w[2].get()
	def get_conditions(self):
		return self.values()

	def close_window(self):
		self.save_changes()
		self.window.destroy()