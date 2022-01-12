from tkinter import *
from tkinter import ttk
import sqlite3




# Connect to Database
def create_connection(pathToDataBase):
    connection = None
    try:
        connection = sqlite3.connect(pathToDataBase)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
        
    return connection

connection = create_connection('hgp.sqlite3')

#connection = sqlite3.connect('hgp.sqlite3')
cursor = connection.cursor()

# Execute Queries

def create_tables():
    cursor.execute('create table if not exists checks (chkId integer primary key,chkNbr text,payee text,chkAmt double,chkCmt text)')
    cursor.execute('create table if not exists  accounts (acctId integer primary key,chkNbr,acctNbr text,actAmt double,acctCmt text)')




def execute_query(connection, query):
#    cursor = conection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_drop():
    print('dropping')
    execute_query(connection,'drop table checks')
    execute_query(connection,'drop table accounts')
    quit()

def execute_read_query(connection, query):
#    cursor = connection.cursor()
    result = None
    try:
#        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def post(*args):
    try:
        ''' Get data from Check and Account Fields '''
        check = (chkNbr.get(),payee.get(),chkAmt.get(),chkCmt.get())
        account = (chkNbr.get(),acctNbr.get(),actAmt.get(),acctCmt.get())

        ''' Sql commands to add records to data base '''
        cursor.execute('insert into checks(chkNbr,payee,chkAmt,chkCmt) values (?,?,?,?)',check)
        cursor.execute('insert into accounts(chkNbr,acctNbr,actAmt,acctCmt) values (?,?,?,?)',account)

        ''' SQL command to select all rows from Checks table then
            Loop through result set to printout Checks data '''
        cursor.execute('Select checks.chkNbr, payee, chkAmt,acctNbr,actAmt from checks,accounts where checks.chkNbr = accounts.chkNbr')
        for row in cursor:
            item = ''
            for items in row:
                item = item + ' ' + str(items)
            print(item)

        ''' SQL command to select all rows from Accounts table then
            loop through result set to printout the Accounts data '''
        cursor.execute('Select * from accounts')
        for row in cursor:
            item = ''
            for items in row:
                item = item + ' ' + str(items)
            print(item)

        chkNbr.set('')
        payee.set('')
        chkAmt.set(0.00)
        chkCmt.set('')
        acctNbr.set('')
        actAmt.set(0.00)
        acctCmt.set('')


        cursor.close
    except ValueError:
        pass

    
root = Tk()
root.title("Checkesi")

create_tables()

''' Initialize field variables '''
chkNbr = StringVar()
payee = StringVar()
chkAmt  = DoubleVar()
chkCmt = StringVar()
acctNbr = StringVar()
actAmt = DoubleVar()
acctCmt = StringVar()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

''' Add Labels, Buttons and Fields to GUI '''
ttk.Label(mainframe, text="Check: ").grid(column=1, row=1, sticky=W)
chkNbr_entry = ttk.Entry(mainframe, width=7, textvariable=chkNbr)
chkNbr_entry.grid(column=2, row=1, sticky=(W, E))

ttk.Label(mainframe, text="Payee: ").grid(column=1, row=2, sticky=W)
payee_entry = ttk.Entry(mainframe, width=15, textvariable=payee)
payee_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Label(mainframe, text="Amount: ").grid(column=1, row=3, sticky=W)
chkAmt_entry = ttk.Entry(mainframe, width=15, textvariable=chkAmt)
chkAmt_entry.grid(column=2, row=3, sticky=(E))

ttk.Label(mainframe, text="Comment: ").grid(column=1, row=4, sticky=W)
chkCmt_entry = ttk.Entry(mainframe, width=7, textvariable=chkCmt)
chkCmt_entry.grid(column=2, row=4, sticky=(W, E))

ttk.Label(mainframe, text="Account: ").grid(column=1, row=5, sticky=W)
account_entry = ttk.Entry(mainframe, width=7, textvariable=acctNbr)
account_entry.grid(column=2, row=5, sticky=(W, E))

ttk.Label(mainframe, text="Amount: ").grid(column=1, row=6, sticky=W)
actAmt_entry = ttk.Entry(mainframe, width=15, textvariable=actAmt)
actAmt_entry.grid(column=2, row=6, sticky=(E))

ttk.Label(mainframe, text="Comment: ").grid(column=1, row=7, sticky=W)
chkCmt_entry = ttk.Entry(mainframe, width=7, textvariable=acctCmt)
chkCmt_entry.grid(column=2, row=7, sticky=(W, E))

ttk.Button(mainframe, text="POST", command=post).grid(column=1, row=8, sticky=W)
ttk.Button(mainframe, text="EXIT", command=execute_drop).grid(column=2, row=8, sticky=E)
# ttk.Button(mainframe, text="Clear", command=execute_drop).grid(column=3, row=8, sticky=W)


#for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

chkNbr_entry.focus()
root.bind('<Return>', post)

root.mainloop()
