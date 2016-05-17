from tkinter import *
import logging
from classes.program import PhotoOrganizer

logging.basicConfig(filename='logging.log',level=logging.INFO, format='[%(asctime)s] %(message)s')
logging.info('Starting')
PhotoOrganizer(Tk())
logging.info('Done')
