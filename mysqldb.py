from flask_mysqldb import MySQL
import mysql.connector

test = mysql.connector.connect(
    host= "localhost" ,
    user = "admin" ,
    passwd = "admin" ,
    database = "test"
)
c = test.cursor()


c.execute('''drop table if exists users ''')
c.execute('''    CREATE TABLE users(
        id INT AUTO_INCREMENT PRIMARY KEY ,
        username VARCHAR(255) UNIQUE ,
        password VARCHAR(255) NOT NULL,
        dept_id INT ,
        user_id INT ) ''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
              VALUES ('admin','admin',1,1)''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
              VALUES ('user1','100',2,2)''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
             VALUES ('user2','200',3,3)''')

#fetch data from users tables
c.execute("SELECT * FROM users ")
rows = c.fetchall()
print(rows)
# Create table departments
c.execute(''' drop table if exists departments ''')
c.execute(''' CREATE TABLE departments (
               dept_id INT PRIMARY KEY ,
               dept_name TEXT NOT NULL ); ''')
c.execute(''' INSERT INTO departments(dept_id,dept_name)
                VALUES (1,'admin')''')
c.execute(''' INSERT INTO departments(dept_id,dept_name)
                VALUES (2,'sales')''')
c.execute(''' INSERT INTO departments(dept_id,dept_name)
                VALUES (3,'development')''')

# Fetch all data from departments 
c.execute("SELECT * FROM departments ")
rows = c.fetchall()
print(rows)

#Create table user_profile
c.execute (''' drop table if exists user_profile ''')
c.execute (''' CREATE TABLE user_profile (
                prof_id INT PRIMARY KEY ,
                prof_name TEXT ,
                is_admin INT ) ''')
c.execute(''' INSERT INTO user_profile(prof_id,prof_name,is_admin)
                VALUES (1,'Manager',1)''')
c.execute(''' INSERT INTO user_profile(prof_id,prof_name,is_admin)
                VALUES (2,'Sales',0)''')
c.execute(''' INSERT INTO user_profile(prof_id,prof_name,is_admin)
                VALUES (3,'Developer',0)''')

#Fetch all data from user_profile
c.execute("SELECT * FROM user_profile")
rows = c.fetchall()
print(rows)

#show table:
c.execute("SHOW TABLES")
for x in c :
    print(x)

test.close()
