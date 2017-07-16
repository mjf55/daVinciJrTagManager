import sqlite3

def connect():  # this is working, but need to think about unique values to not duplicate on update
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS tagdata ( UID1 TEXT, UID2 TEXT, Pword TEXT, PACK TEXT, Used TEXT, UIDall TEXT UNIQUE)")
	conn.commit()
	conn.close()
	
def  insert( status, UID1, UID2, Pword, PACK, Used): 
	UIDall = UID1+UID2+Pword+PACK
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("INSERT OR IGNORE INTO tagdata VALUES ( ?, ?, ?, ?, ?, ?)",  (UID1, UID2, Pword, PACK, Used, UIDall))
	conn.commit()
	conn.close()
	status.set("Status: Record Inserted into the database")


def  update(status, oid, UID1, UID2, Pword, PACK, Used):  
	UIDall = UID1+UID2+Pword+PACK
	conn=sqlite3.connect("davincipw.db")
	cur=conn.cursor()
	cur.execute("UPDATE tagdata SET UID1=?, UID2=?, Pword=?, PACK=?, Used=? WHERE oid =?" , (UID1, UID2, Pword, PACK, Used, oid))
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
	cur.execute("UPDATE tagdata set Used='Used' WHERE oid=? ", (oid,))
	rows = cur.fetchone() 
	conn.commit()
	conn.close()
	status.set("Status: This UID has been marked USED")
	
def search(status, listbox, END, oid, UID1, UID2, Pword, PACK, Used):
	conn=sqlite3.connect("davincipw.db")
	conn.text_factory = str   # gets rid of the u in the data (unicode) for fetchall
	cur=conn.cursor()
	cur.execute("SELECT oid, UID1, UID2, Pword, PACK, Used FROM tagdata WHERE oid=? OR UID1=? OR UID2=? OR Pword=? OR PACK=? ", (oid, UID1, UID2, Pword, PACK))
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
	