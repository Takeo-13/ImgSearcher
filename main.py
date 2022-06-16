import tkinter.messagebox
from translate import Translator
from random import choice as chs
import webbrowser
import os, os.path
import threading

import scrapper
from scrapper import *

import tkinter as tk
from tkinter import ttk
from tkinter import *

import threading

class Application:

    # this is a function to get the user input from the text input box
    def getProxyBoxValue(self):
        userInput = self.proxyVar.get()
        return userInput


    # this is the function called when the button is clicked
    def opengitrep(self):
        webbrowser.open('https://github.com/Takeo-13/ImgSearcher')


    # this is the function called when the button is clicked
    def createBill(self):
        tkinter.messagebox.showinfo('Click!', 'Click!')


    # this is the function called when the button is clicked
    def openArchives(self):
        webbrowser.open('https://gymnasium.msu.ru')

    # this is the function called when the button is clicked
    def startScrapping(self):
        tkinter.messagebox.showinfo('A little patience!', 'Now wait while the program ends with scrapping, please!')
        if self.numVar.get().isdigit() != True:
            tkinter.messagebox.showerror('It must be a number!')
            return

        tr = Translator(to_lang="en")
        threading.Thread(target=scrapper.grab, args=(tr.translate(self.filterVar.get()), int(self.numVar.get()))).start()
        threading.Thread(target=scrapper.grab, args=(self.filterVar.get(), int(self.numVar.get()))).start()


    # This is a function which increases the progress bar value by the given increment amount
    def makeProgress(self):
        self.scrapProgress['value'] += 1
        root.update_idletasks()

    def __init__(self, master=None):
        # This is the section of code which creates the a label
        Label(root, text='Filter:', bg='#808086', font=('arial', 9, 'normal')).place(x=26, y=30)

        Label(root, text='Path to proxy file:', bg='#808086', font=('arial', 9, 'normal')).place(x=26, y=65)

        Label(root, text="Number of pages: ", bg='#808086', font=('arial', 9, 'normal')).place(x=26, y=100)

        Label(root, text="(c) Takeo-13 (s4lieri) & Shirime-san Goddess", bg='#808086', font=('arial', 8, 'normal')).place(x=30, y=340)

        self.filterVar = Entry(root)
        self.filterVar.place(x=147, y=30)

        self.numVar = Entry(root)
        self.numVar.place(x=147, y=102)

        self.proxyVar=Entry(root, textvariable="Currently Unavailable", state='disabled')
        self.proxyVar.place(x=147, y=65)


        # This is the section of code which creates a button
        Button(root, text='GitHub Repository', bg='#DEDEDE', font=('arial', 8, 'normal'), command=self.opengitrep).place(x=196, y=399)

        Button(root, text='Click!', bg='#DEDEDE', font=('arial', 8, 'normal'), command=self.createBill).place(x=6, y=399)

        Button(root, text='Archives', bg='#FFFFFF', font=('arial', 8, 'normal'), command=self.openArchives).place(x=114, y=399)

        Button(root, text='Start scrapping', bg='#CCCCCC', font=('arial', 8, 'normal'), command=self.startScrapping).place(x=107, y=244)


        # This is the section of code which creates a color style to be used with the progress bar
        self.scrapProgress_style = ttk.Style()
        self.scrapProgress_style.theme_use('clam')
        self.scrapProgress_style.configure('scrapProgress.Horizontal.TProgressbar', foreground='#CCCCCC', background='#CCCCCC')


        # This is the section of code which creates a progress bar
        self.scrapProgress=ttk.Progressbar(root, style='scrapProgress.Horizontal.TProgressbar', orient='horizontal', length=299, mode='determinate', maximum=100, value=1)
        self.scrapProgress.place(x=10, y=275, width=280, height=25)

if __name__ == "__main__":
    root = Tk()

    # This is the section of code which creates the main window
    root.geometry('300x428')
    root.configure(background='#808086')
    root.title(chs(['Shira', 'AcuteEye', 'Blind (?) Eye', 'Evil (?!) Eye', 'A Cute Eye!']))
    root.resizable(False, False)

    app = Application(master=root)
    root.mainloop()