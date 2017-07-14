#!/usr/bin/env python

from Tkinter import *
import Tkinter, Tkconstants, tkFileDialog
from myFunctions import *
from SQLbackend import *

#Create the window object    # All windows object between window=Tk() and window.mainloop()
window=Tk()
window.geometry("650x400")
window.title("DaVinci Jr Password Manager")

temperature=IntVar()
spoolsize=IntVar()
sStatus=StringVar()

# Menu System
menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Create Database", command=lambda: importCSV(sStatus, window, tkFileDialog)) 
filemenu.add_command(label="Import new CVS", command=lambda: importCSV(sStatus, window, tkFileDialog))

filemenu.add_separator()

filemenu.add_command(label="Exit", command=lambda: myExit(window)) 

menubar.add_cascade(label="File", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=lambda: notyet(window))
helpmenu.add_command(label="About...", command=lambda: notyet(window))
menubar.add_cascade(label="Help", menu=helpmenu)

window.config(menu=menubar)

# define labels
l1=Label(window, text="id")
l1.grid(row=1, column=1, sticky=E)

l2=Label(window, text="UID-1")
l2.grid(row=2, column=1, sticky=E)

l3=Label(window, text="UID-2")
l3.grid(row=3, column=1, sticky=E)

l4=Label(window, text="Password")
l4.grid(row=4, column=1, sticky=E)

l5=Label(window, text="PACK")
l5.grid(row=5, column=1, sticky=E)

lUsed=Label(window, text="Used")
lUsed.grid(row=6, column=1, sticky=E)

l6=Label(window, text="Page 9 Data")
l6.grid(row=7, column=1, sticky=E)

lSearchResults=Label(window, text="Search Results")
lSearchResults.grid(row=9, column=0)

sStatus.set('Status:')
lStatus=Label(window, textvariable=sStatus)
lStatus.grid(row=21, column=0, columnspan=3, sticky=W)

# define entries
id_text=IntVar()
e1=Entry(window, textvariable=id_text)
id_text.set("")
e1.grid(row=1, column=2)

UID1_text=StringVar()
e2=Entry(window, textvariable=UID1_text)
e2.grid(row=2, column=2)

UID2_text=StringVar()
e3=Entry(window, textvariable=UID2_text)
e3.grid(row=3, column=2)

password_text=StringVar()
e4=Entry(window, textvariable=password_text)
e4.grid(row=4, column=2)

pack_text=StringVar()
e5=Entry(window, textvariable=pack_text)
e5.grid(row=5, column=2)

used_text=StringVar()
e6=Entry(window, textvariable=used_text)
e6.grid(row=6, column=2)

page9_text=StringVar()
e7=Entry(window, textvariable=page9_text)
e7.grid(row=7, column=2)


# define ListBox and scroll bar
list1=Listbox(window, height=10, width=40)
list1.grid(row=10, column=0, rowspan=10, columnspan=2)
list1.bind('<<ListboxSelect>>', lambda event: onselect(event, id_text, UID1_text, UID2_text, password_text, pack_text, used_text ))

sb1=Scrollbar(window)
sb1.grid(row=10, column=2, rowspan=10, sticky=W, ipady = 60)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

# define buttons
b1=Button(window, text="Get New UID", bg='green', width=16, command=lambda: newUID(sStatus, id_text, UID1_text, UID2_text, password_text, pack_text))
b1.grid(row=11, column=4)

b2=Button(window, text="Use This UID", bg='green', width=16, command=lambda: useUID(sStatus, int(e1.get())))
b2.grid(row=11, column=5)

b7=Button(window, text="Generate Tagdata", bg='green', width=16, command=lambda: generateTagData(sStatus, e2.get(), e3.get(), e4.get(), e5.get() , str(temperature.get()), str(spoolsize.get()), e7.get()))
b7.grid(row=12, column=4)

b8=Button(window, text="Program EMUtag", bg='green', width=16, state=DISABLED, command=lambda: notyet(window))
b8.grid(row=12, column=5)

b3=Button(window, text="Search Database" , bg='yellow', width=16, command=lambda: search(sStatus, list1, END,  e1.get(),e2.get(), e3.get(), e4.get(), e5.get(),e6.get() ))
b3.grid(row=13, column=4)

b4=Button(window, text="View All", bg='yellow', width=16, command=lambda: view(sStatus, window, list1, END))
b4.grid(row=13, column=5)

b5=Button(window, text="Update Record", bg='yellow', width=16, command=lambda: update(sStatus, e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get()))
b5.grid(row=14, column=4)

b6=Button(window, text="Insert Record", bg='yellow', width=16, command=lambda: insert(sStatus, e2.get(), e3.get(), e4.get(), e5.get(), e6.get()))
b6.grid(row=14, column=5)

b9=Button(window, text="Exit", bg='green', width=16, command=lambda: myExit(window))
b9.grid(row=15, column=5)

b10=Button(window, text="Delete Record", bg='red', width=16, command=lambda: myDelete(sStatus, e1.get()))
b10.grid(row=15, column=4)

# define Radio Buttons and label
lTemp=Label(window, text="Filament Temperature")
lTemp.grid(row=1, column=4, sticky=E, columnspan=2)

rTempLow = Radiobutton(window, text="190*", value=190, variable = temperature)
rTempLow.grid(row=2, column=4, sticky=E)
temperature.set(190)

rTempHi = Radiobutton(window, text="210*", value=210, variable = temperature)
rTempHi.grid(row=2, column=5, sticky=E)

lSpool=Label(window, text="      Spool Size")
lSpool.grid(row=4, column=4, columnspan=2)

rSpool200 = Radiobutton(window, text="200M", value=200, variable = spoolsize)
rSpool200.grid(row=5, column=4, sticky=E)

rSpool300 = Radiobutton(window, text="300M", value=300, variable = spoolsize)
rSpool300.grid(row=5, column=5, sticky=E)
spoolsize.set(300)

#end of window object
window.mainloop()
