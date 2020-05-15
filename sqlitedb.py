import sqlite3 as sql

con = sql.connect('users.db')
print("opened db successfully");
print(con)

c =  con.cursor()

# Create table - Users
c.execute('''drop table if exists users ''')
c.execute('''    CREATE TABLE users(
        id INTEGER PRIMARY KEY ,
        username  NOT NULL UNIQUE ,
        password  NOT NULL
        );''')
c.execute('''INSERT INTO users(username,password)
              VALUES ('admin','100')''')
c.execute('''INSERT INTO users(username,password)
              VALUES ('user1','test')''')

#fetch all data from table:
c.execute("SELECT * FROM users ")
rows = c.fetchall()
print(rows)

con.commit()
con.close()
