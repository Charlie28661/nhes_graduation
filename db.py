import sqlite3

#init
def create_table():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('''CREATE TABLE users
                (ID text, CLASS text, NAME text)''')
    cur.execute("INSERT INTO users VALUES ('','','')")
    con.commit()
    con.close()

#create_table()

