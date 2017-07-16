import  csv
from SQLbackend import connect, insert, delete
import tkMessageBox
import os

def notyet(window):
	tkMessageBox.showinfo(title="Function Not Supported", message='Sorry, I have not implimented this function yet')
	return
	
def myExit(window):
	# does not work  window not defined
	print "See ya later, Alligator"
	window.quit()

def myDelete(status, oid):
	mDelete = tkMessageBox.askyesno(title="Delete Record", message='Are you sure?')
	if mDelete > 0:
		delete(status, oid)
		return
	
def dbCreateUpdate(status, window, FD):

	status.set("Status: This may take awhile")

	#now lets open the csv file and  create / update  the database
	fname= FD.askopenfilename(initialdir = ".",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
	connect()
	with open(fname, 'rb') as csvfile:  
		for line in csvfile.readlines():
			array = line.split(',')
			if array[0] == "4":  					# first byte must be 4
				for x in range(0 , len(array)):
					if len(array[x] ) ==  1:
						array[x] = '0' + array[x]  # make sure there are 2 characters

				UID1 = array[0]  + array[1] + array[2]
				UID2 = array[3]  + array[4] + array[5] + array[6]
				Pword = array[8]  + array[9] + array[10] + array[11]
				tempPACK= array[13]  + array[14] 
				Used = ""
				PACK = tempPACK.rstrip()
				# Use only if there is a PACK valid -> Record is valid
				if PACK:
					insert(status, UID1.rstrip(), UID2.rstrip(), Pword.rstrip(), PACK.rstrip(), Used)
	status.set("Status: Database updated")

	
def onselect(evt, id, uid1, uid2, pword, pack, used):
	w = evt.widget
	index = int(w.curselection()[0])
	value = w.get(index)
	id.set(value[0])
	uid1.set(value[1])
	uid2.set(value[2])
	pword.set(value[3])
	pack.set(value[4])
	used.set(value[5])


def generateTagData(status, uid1, uid2, pword, pack, temperature, spoolsize, page9):
	#Page  300m/300m		200m/200/		PLA/190*		PLA/210*
	#10,11 E0930400			00030d40
	#20    E0930400			00030d40
	#21    A8813654			081F3154
	#22    F03FEECE			50B1E0CE
	#23    F26E4D76			52E74F76
	#08										5A504800	5A504F00

	word = ['04A0B961', '229A3D80', '79480000', 'E1101200', '0103A00C', '340300FE', '00000000', '00000000',
			'5A505A00', '0035344A', 'E0930400', 'E0930400', 'D2002D00', '54484742', 'E09304FF', '00000000',
			'00000000', '34000000', '00000000', '00000000', 'E0930400', 'A8813654', 'F03FEECE', 'F26E4D76',
			'00000000', '00000000', '00000000', '00000000', '00000000', '000000FF', '00000000', '00000000',
			'00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000', '00000000',
			'000000BD', '070000FF', '80050000', '0D02FB70', '6B680000']
	word[0] = (uid1 + "AA").rstrip()
	word[1] = uid2.rstrip()
	if temperature == "210":
		print "temperature = 210"
		word[8] = '5A504F00'
	if spoolsize == "200":
		print "Spoolsize = 200"
		word[10] = '00030D40'
		word[11] = '00030D40'
		word[20] = '00030D40'
		word[21] = '081F3154'
		word[22] = '50B1E0CE'
		word[23] = '52E74F76'
	if page9 != "":
		print "updating page 9"
		word[9] = page9
	word[43] = pword.rstrip()
	word[44] = (pack + "0000").rstrip()

	#Write the data to the file
	# we need only a \n = 0A = chr(10) for the line termination
	# character.  In windows it will put \r\n.  Using chr(10) to 
	#force only the 0A.  Also, do not want it on the last line
	# Word is 45 pages 0 based so it is 0-44.  sub 1 from len(word)
	# to get last page  The resulting txt file is 404 bytes
	fname=uid1 + 'tagdata.txt'
	f1=open(fname, 'wb')
	for x in range(len(word)-1):  
		f1.write(word[x]  + chr(10))
	f1.write(word[len(word)-1])  
	f1.close()
	status.set("Status: New tag data written as " + fname)


def clearEntry(sStatus, END, id, uid1, uid2, pword, pack, used, page9):
	id.delete(0,END)
	uid1.delete(0,END)
	uid2.delete(0,END)
	pword.delete(0,END)
	pack.delete(0,END)
	used.delete(0,END)
	page9.delete(0,END)