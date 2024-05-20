from tkinter import *
from tkinter import messagebox
from datetime import datetime as dt
import sqlite3

connect = sqlite3.connect('pets.db')
cursor = connect.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS PetInformation (id INTEGER PRIMARY KEY, owner TEXT NOT NULL, petname TEXT NOT NULL, pettype TEXT NOT NULL, dateadded TEXT NOT NULL)""")
connect.commit()


root = Tk()
root.title('Pet Information Management')
root.config(bg = 'lightblue')
root.geometry('400x500')
root.resizable(False, False)

def add():
    def close():
        ownerlbl.destroy()
        owner.destroy()
        petnamelbl.destroy()
        petname.destroy()
        pettypelbl.destroy()
        pettype.destroy()
        adddata.destroy()
        deletedata.destroy()

    def addrecord():
        connect = sqlite3.connect('pets.db')
        cursor = connect.cursor()
        ownername = owner.get().title()
        petname1 = petname.get().title()
        pettype1 = pettype.get().title()
        current_date = dt.now().strftime('%Y-%m-%d')
        cursor.execute('select * from PetInformation where owner = ? and petname = ? and pettype = ?', (ownername, petname1, pettype1,))
        check = cursor.fetchall()
        check = int(len(check))
        if ownername == '' or petname1 == '' or pettype1 == '':
            messagebox.showerror(title = "Missing Input", message = "Entry can not be empty!")
        elif check == 0:
            cursor.execute("""INSERT INTO PetInformation
                        (owner, petname, pettype, dateadded) VALUES
                        (?, ?, ?, ?)""", (ownername, petname1, pettype1, current_date))
            connect.commit()
            messagebox.showinfo(title = "Success", message = "Successfully recorded to database!")
            close()
        else:
            messagebox.showerror(title = "Already Exist", message = "Data already exist!")
        

    def deleterecord():
        connect = sqlite3.connect('pets.db')
        cursor = connect.cursor()
        ownername = owner.get().title()
        petname1 = petname.get().title()
        pettype1 = pettype.get().title()
        cursor.execute('select * from PetInformation where owner = "{ownername}" and petname = "{petname1}" and pettype = "{pettype1}"')
        check = cursor.fetchall()
        check = str(check)
        if ownername == '' or petname1 == '' or pettype1 == '':
            messagebox.showerror(title = "Missing Input", message = "Entry can not be empty!")
        elif check != '[]':
            cursor.execute("delete from PetInformation where owner = ? and petname = ? and pettype = ?", (ownername, petname1, pettype1,))
            connect.commit()
            messagebox.showinfo(title = "Delete Success!", message = "Data deleted from database!")
            close()
        else:
            messagebox.showerror(title = "No data found!", message = 'Data does not exist!')
        
            


    cursor.execute('''SELECT MAX(id) FROM PetInformation''')
    id = cursor.fetchone()[0]
    if id == None:
        id = 1
    else:
        id += 1

    ownerlbl = Label(root, text = 'Owner Name:')
    ownerlbl.place(x = 20, y = 100)
    owner = Entry(root, width = 40)
    owner.place(x = 110, y = 100)
    petnamelbl = Label(root, text = 'Pet Name:')
    petnamelbl.place(x = 20, y = 140)
    petname = Entry(root, width = 40)
    petname.place(x = 110, y = 140)
    pettypelbl = Label(root, text = 'Pet Type:')
    pettypelbl.place(x = 20, y = 180)
    pettype = Entry(root, width = 40)
    pettype.place(x = 110, y = 180)
    adddata = Button(root, text = 'Add Data', command = addrecord)
    adddata.place(x = 140, y = 220)
    deletedata = Button(root, text = 'Delete Data', command = deleterecord)
    deletedata.place(x = 220, y = 220)


def view():
    top = Toplevel()
    top.geometry("640x400")
    top.config(bg = 'pink')
    top.resizable(False, False)
    
    def lb():
        listbox.delete(0, END)
        cursor.execute('select * from PetInformation')
        r = cursor.fetchall()
        for x in r:
            listbox.insert(END, f"ID: {x[0]} | Owner Name: {x[1]} | Pet Name: {x[2]} | Pet Type: {x[3]} | Recorded: {x[4]}")

    

    listbox = Listbox(top, width = 100, height = 250, bg = 'pink', fg = 'white', font = ('arial', 9))
    listbox.place(x = 10, y = 10)
    lb()
    top.mainloop()

viewrecord = Button(root, text = 'View Records', fg = 'white', bg = 'teal', command = view)
viewrecord.place(x = 300, y = 10)

newremove = Button(root, text = 'New/Remove', fg = 'white', bg = 'teal', command = add)
newremove.place(x = 200, y = 10)


root.mainloop()