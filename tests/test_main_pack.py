from turtle import width
from numpy import record
import psycopg2
import psycopg2.extras
import os
from tkinter import *
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.messagebox import showinfo

ws = Tk() 
ws.title("Name Pronounciation Tool")
width= ws.winfo_screenwidth()
height= ws.winfo_screenheight()
ws.geometry("%dx%d" % (width, height))
image_mainwindows = PhotoImage(file = os.path.join('data/' + 'logo_icon.png'))

ws.iconphoto(False, image_mainwindows)

#=====================================METHODS==============================================
# def connect_db(conf):
#     print(">>>> Connecting to YugabyteDB!")

#     try:
#         if conf['sslMode'] != '':
#             yb = psycopg2.connect(host=conf['host'], port=conf['port'], database=conf['dbName'],
#                                   user=conf['dbUser'], password=conf['dbPassword'],
#                                   sslmode=conf['sslMode'], sslrootcert=conf['sslRootCert'],
#                                   connect_timeout=10)
#         else:
#             yb = psycopg2.connect(host=conf['host'], port=conf['port'], database=conf['dbName'],
#                                   user=conf['dbUser'], password=conf['dbPassword'],
#                                   connect_timeout=10)
#     except Exception as e:
#         print("Exception while connecting to YugabyteDB")
#         print(e)
#         exit(1)

#     print(">>>> Successfully connected to YugabyteDB!")

#     #create_database(yb)
#     Database(yb)
#     #Database_fname(yb)
#     yb.close()


def create_database(yb):
    try:
        with yb.cursor() as yb_cursor:
            yb_cursor.execute('DROP TABLE IF EXISTS employeeDB')

            create_table_stmt = """CREATE TABLE employeeDB ( empid int PRIMARY KEY, fname varchar, lname varchar, uname varchar, pref_audio varchar)"""
            yb_cursor.execute(create_table_stmt)

            insert_stmt = """
                INSERT INTO employeeDB VALUES
                        (1000000, 'Jessica', 'Jessica', 'j000001',1),
                        (1000002, 'Jessica', 'Pearson', 'j000003',1),
                        (1000001, 'John', 'John', 'j000002',0)"""
            yb_cursor.execute(insert_stmt)
        yb.commit()
    except Exception as e:
        print("Exception while creating tables")
        print(e)
        exit(1)

    print(">>>> Successfully created table employeeDB.")

def item_selected(event):
    for selected_item in tree.selection():
        item = tree.item(selected_item)
        record = item['values']
    print(record)
        # show a message
        #showinfo(title='Information', message=','.join(record))
    return

def selectItem(a):
    curItem = tree.focus()
    print(tree.item(curItem))

def Database(yb):
    with yb.cursor() as yb_cursor:
        yb_cursor.execute("SELECT * FROM employeeDB") 
        yb_cursor.execute("SELECT * FROM employeeDB ORDER BY empid ASC")
        fetch = yb_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        yb_cursor.close()
    return

def Database_fname(yb,str):
    reserTree()
    with yb.cursor() as yb_cursor:
        yb_cursor.execute("SELECT * FROM employeeDB WHERE UPPER(fname) LIKE UPPER('%" + str + "%')")
        fetch = yb_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        yb_cursor.close()
    
def Database_lname(yb,str):
    reserTree()
    with yb.cursor() as yb_cursor:
        yb_cursor.execute("SELECT * FROM employeeDB WHERE UPPER(lname) LIKE UPPER('%" + str + "%')")
        fetch = yb_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        yb_cursor.close()

def Database_empid(yb,int):
    reserTree()
    try:
        with yb.cursor() as yb_cursor:
            yb_cursor.execute("SELECT * FROM employeeDB WHERE empid = '" + int + "'")
            fetch = yb_cursor.fetchall()
            for data in fetch:
                tree.insert('', 'end', values=(data))
            yb_cursor.close()
    except Exception as e:
        print("Exception while creating tables")
        print(e)
        ws.quit()


def Database_uname(yb,str):
    reserTree()
    with yb.cursor() as yb_cursor:
        yb_cursor.execute("SELECT * FROM employeeDB WHERE UPPER(uname) LIKE UPPER('%" + str + "%')")
        fetch = yb_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        yb_cursor.close()


def reserTree():
    tree.delete(*tree.get_children())

def openNewWindow():
    newWindow = Toplevel(ws)
    newWindow.title("Name Pronounciation Tool")
    newWindow.geometry("400x600")
    Label(newWindow,text ="User Detials").pack()
    Label(newWindow, text="Last Name: " + record,font=("Arial", 10)).pack()
    Entry(newWindow, font=("Arial", 10),width=50)
    Button(newWindow, text ="Search",width=20)#,command=lambda : Database_lname(yb,entry_lname.get()))


def say_my_name(str):
    try:
        engine = pyttsx3.init()
        rate = engine.getProperty('rate')
        engine.setProperty('rate', 125)
        volume = engine.getProperty('volume')
        engine.setProperty('volume',1.0)   
        #voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        name = str
        engine.say(name)
        engine.runAndWait()
        engine.stop()
        engine.runAndWait()
    except Exception as e:
        print("Exception while creating tables")
        print(e)
        exit(1)

#=====================================VARIABLES============================================
config = {                                  ## yugabytedb connection
    'host': '127.0.0.1',
    'port': '5433',
    'dbName': 'yugabyte',
    'dbUser': 'yugabyte',
    'dbPassword': 'yugabyte',
    'sslMode': '',
    'sslRootCert': ''
}

try:
    if config['sslMode'] != '':
        yb = psycopg2.connect(host=config['host'], port=config['port'], database=config['dbName'],
                                user=config['dbUser'], password=config['dbPassword'],
                                sslmode=config['sslMode'], sslrootcert=config['sslRootCert'],
                                connect_timeout=10)
    else:
        yb = psycopg2.connect(host=config['host'], port=config['port'], database=config['dbName'],
                                user=config['dbUser'], password=config['dbPassword'],
                                connect_timeout=10)
except Exception as e:
    print("Exception while connecting to YugabyteDB")
    print(e)
    exit(1)

print(">>>> Successfully connected to YugabyteDB!")

SEARCH = StringVar()

#=====================================Menu Bar============================================
menubar = Menu(ws)
file1 = Menu(menubar, tearoff=0)

file1.add_command(label="Exit", command=ws.quit)

menubar.add_cascade(label="File", menu=file1)
edit1 = Menu(menubar, tearoff=0)

help1 = Menu(menubar, tearoff=0)
help1.add_command(label="About")
menubar.add_cascade(label="Help", menu=help1)

ws.config(menu=menubar)

#=====================================LABEL WIDGET=========================================
label_search = Label(ws, text="Search...",font=("Arial", 10,"bold"))
label_search.pack(padx=5, pady=15)#.grid(row=0, column=1,padx=5, pady=15)

separator = ttk.Separator(ws, orient='horizontal')
separator.pack(fill='x', padx=5, pady=10)

# First Name
label_fname = Label(ws, text="First Name",font=("Arial", 10))
label_fname.pack(padx=5, pady=5)#.grid(row=1, column=1, padx=5, pady=15)
entry_fname = Entry(ws, font=("Arial", 10))
entry_fname.pack(padx=5, pady=5,fill='x')#.grid(row=1, column=2, padx=15, pady=15)
button_fname = Button(ws, text ="Search",width=20,command=lambda : Database_fname(yb,entry_fname.get()))
button_fname.pack(padx=5, pady=5)#.grid(row=1, column=3, padx=5, pady=15)
separator = ttk.Separator(ws, orient='horizontal')
separator.pack(fill='x', padx=5, pady=10)

# Last Name
label_lname = Label(ws, text="Last Name",font=("Arial", 10))
label_lname.pack(padx=5, pady=5)#.grid(row=2, column=1, padx=5, pady=15)
entry_lname = Entry(ws, font=("Arial", 10),width=50)
entry_lname.pack(padx=5, pady=5,fill='x')#.grid(row=2, column=2, padx=5, pady=15)
button_lname = Button(ws, text ="Search",width=20,command=lambda : Database_lname(yb,entry_lname.get()))
button_lname.pack(padx=5, pady=5)#.grid(row=2, column=3, padx=5, pady=15)
separator = ttk.Separator(ws, orient='horizontal')
separator.pack(fill='x', padx=5, pady=10)

# User Name
label_uname = Label(ws, text="User Name",font=("Arial", 10))
label_uname.pack(padx=5, pady=5)#.grid(row=4, column=1, padx=5, pady=15)
entry_uname = Entry(ws, font=("Arial", 10),width=50)
entry_uname.pack(padx=5, pady=5,fill='x')#.grid(row=3, column=2, padx=5, pady=15)
button_uname = Button(ws, text ="Search",width=20,command=lambda : Database_uname(yb,entry_uname.get()))
button_uname.pack(padx=5, pady=5)#.grid(row=4, column=3, padx=5, pady=15)
separator = ttk.Separator(ws, orient='horizontal')
separator.pack(fill='x', padx=5, pady=10)

# Employee ID
label_emp_id = Label(ws, text="Employee ID",font=("Arial", 10))
label_emp_id.pack(padx=5, pady=5)#.grid(row=3, column=1, padx=5, pady=15)
entry_emp_id = Entry(ws, font=("Arial", 10),width=50)
entry_emp_id.pack(padx=5, pady=5,fill='x')#.grid(row=3, column=2, padx=5, pady=15)
button_emp_id= Button(ws, text ="Search",width=20,command=lambda : Database_empid(yb,entry_emp_id.get()))
button_emp_id.pack(padx=5, pady=5)#.grid(row=4, column=3, padx=5, pady=15)
separator = ttk.Separator(ws, orient='horizontal')
separator.pack(fill='x', padx=5, pady=10)

# define columns
columns = ('empid', 'fname', 'lname', 'uname', 'pref_audio')

tree = ttk.Treeview(ws, columns=columns, show='headings')

# define headings
tree.heading('empid', text='Employee ID')
tree.heading('fname', text='First Name')
tree.heading('lname', text='Last Name')
tree.heading('uname', text='User Name')
tree.heading('pref_audio', text='Preferred Name')

tree.bind('<<TreeviewSelect>>', item_selected)

tree.pack(fill='x')#.grid(row=8, column=1, sticky='nsew')

# add a scrollbar
scrollbar = ttk.Scrollbar(ws, orient=tk.VERTICAL, command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack()#.grid(row=8, column=2, sticky='ns')

button_ok = Button(ws, text ="OK", width=20,command = openNewWindow)
button_ok.pack(padx=5, pady=5)

#=====================================Table WIDGET=========================================


log_user = os.getlogin()

#=====================================INITIALIZATION=======================================
if __name__ == '__main__':
    # connect_db(config)
    create_database(yb)
    ws.mainloop()
