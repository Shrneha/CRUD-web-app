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
              VALUES ('admin','admin')''')
c.execute('''INSERT INTO users(username,password)
              VALUES ('user1','100')''')
c.execute('''INSERT INTO users(username,password)
             VALUES ('user2','200')''')

#fetch all data from users table:
c.execute("SELECT * FROM users ")
rows = c.fetchall()
print(rows)

# Create table departments
c.execute(''' drop table if exists departments ''')
c.execute(''' CREATE TABLE departments (
               dept_id INTEGER PRIMARY KEY ,
               dept_name TEXT NOT NULL ); ''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('admin')''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('sales')''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('development')''')

# Fetch all data from departments 
c.execute("SELECT * FROM departments ")
rows = c.fetchall()
print(rows)

#Create table user_profile
c.execute (''' drop table if exists user_profile ''')
c.execute (''' CREATE TABLE user_profile (
                prof_id INTEGER PRIMARY KEY ,
                prof_name TEXT ,
                is_admin NUMBER ); ''')
c.execute(''' INSERT INTO user_profile(prof_name,is_admin)
                VALUES ('Manager',1)''')
c.execute(''' INSERT INTO user_profile(prof_name,is_admin)
                VALUES ('Sales',0)''')
c.execute(''' INSERT INTO user_profile(prof_name,is_admin)
                VALUES ('Developer',0)''')

#Fetch all data from user_profile
c.execute("SELECT * FROM user_profile")
rows = c.fetchall()
print(rows)




con.commit()
con.close()
