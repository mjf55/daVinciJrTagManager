#SQLbackend.py - SQL functions for the daVinciJrTagManager set up programs
#Copyright (C) 2017  Mark Ferrick
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at my option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
from datetime import date

def connect():  # this is working, but need to think about unique values to not duplicate on update
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS tagdata ( UID1 TEXT, UID2 TEXT, Pword TEXT, PACK TEXT, Used TEXT, UIDall TEXT UNIQUE)")
	conn.commit()
	conn.close()
	
def  insert(status, UID1, UID2, Pword, PACK, Used): 
	UIDall = UID1+UID2+Pword+PACK
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("INSERT OR IGNORE INTO tagdata VALUES ( ?, ?, ?, ?, ?, ?)",  (UID1.upper(), UID2.upper(), Pword.upper(), PACK.upper(), Used, UIDall.upper()))
	conn.commit()
	conn.close()
	status.set("Status: Record Inserted into the database")


def  update(status, oid, UID1, UID2, Pword, PACK, Used):  
	UIDall = UID1+UID2+Pword+PACK
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("UPDATE tagdata SET UID1=?, UID2=?, Pword=?, PACK=?, Used=? WHERE oid =?" , (UID1.upper(), UID2.upper(), Pword.upper(), PACK.upper(),  Used, oid))
	conn.commit()
	conn.close()
	status.set("Status: Record has been updated")

def  view(status, window, listbox, END):  
	conn=sqlite3.connect("davincipw.db")
	conn.text_factory = str   # gets rid of the u in the data (unicode) for fetchall
	cur=conn.cursor()
	cur.execute("SELECT oid, UID1, UID2, Pword, PACK, Used FROM tagdata")
	rows = cur.fetchall()
	conn.close()
	listbox.delete(0, END)
	for row in rows:
		listbox.insert(END, row)

def newUID(status, oid, uid1, uid2, pword, pack):   
	conn=sqlite3.connect("davincipw.db")
	conn.text_factory = str  # gets rid of the u in the data (unicode) for fetchall
	cur=conn.cursor()
	cur.execute("SELECT oid, UID1, UID2, Pword, PACK FROM tagdata WHERE Used=''")
	rows = cur.fetchone() 
	conn.close()
	oid.set(rows[0])
	uid1.set(rows[1])
	uid2.set(rows[2])
	pword.set(rows[3])
	pack.set(rows[4])
	status.set("Status: newID request complete")

def useUID(status, oid): 
	conn=sqlite3.connect("davincipw.db")
	conn.text_factory = str  # gets rid of the u in the data (unicode) for fetchall
	cur=conn.cursor()
	usedStr = 'Used- ' + str(date.today())
	cur.execute("UPDATE tagdata set Used=? WHERE oid=? ", (usedStr, oid,))
	rows = cur.fetchone() 
	conn.commit()
	conn.close()
	status.set("Status: This UID has been marked USED")
	
def search(status, listbox, END, oid, UID1, UID2, Pword, PACK, Used):
	conn=sqlite3.connect("davincipw.db")
	conn.text_factory = str   # gets rid of the u in the data (unicode) for fetchall
	cur=conn.cursor()
	if Used =="":
		cur.execute("SELECT oid, UID1, UID2, Pword, PACK, Used FROM tagdata WHERE oid=? OR UID1=? OR UID2=? OR Pword=? OR PACK=?  ", (oid, UID1.upper(), UID2.upper(), Pword.upper(), PACK.upper()))
	else:
		cur.execute("SELECT  oid, UID1, UID2, Pword, PACK, Used FROM tagdata WHERE Used LIKE ?", ('%' + Used.upper() + '%',))
	rows = cur.fetchall() 
	conn.close()
	listbox.delete(0, END)
	for row in rows:
		listbox.insert(END, row)
	status.set("Status: Search Complete.  Results in Listbox")
	
def  delete(status, id): 
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("DELETE FROM tagdata WHERE oid=?", (id,))
	conn.commit()
	conn.close()
	status.set("Status: Record has been deleted")
	
