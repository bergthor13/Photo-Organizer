from tkinter import *
import json
from classes.program import PhotoOrganizer

# Load the configuration file.
conf = json.loads(open('config.json').read())

PhotoOrganizer(Tk(), conf)