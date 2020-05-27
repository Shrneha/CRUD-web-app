from flask_mysqldb import MySQL
import mysql.connector
import pandas as pd

test = mysql.connector.connect(
    host= "localhost" ,
    user = "admin" ,
    passwd = "admin" ,
    database = "test"
)
c = test.cursor()

####Create users table 
c.execute('''drop table if exists users ''')
c.execute('''    CREATE TABLE IF NOT EXISTS users(
        id INT(11) auto_increment  ,
        username VARCHAR(255) NOT NULL UNIQUE ,
        password VARCHAR(255) NOT NULL,
        dept_id INT  ,
        user_id INT ,
        PRIMARY KEY(id)
        ) ''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
              VALUES ('admin','admin',1,1)''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
              VALUES ('user1','100',2,2)''')
c.execute('''INSERT INTO users(username,password,dept_id,user_id)
             VALUES ('user2','200',3,3)''')

###fetch data from users tables
c.execute("SELECT * FROM users ")
rows = c.fetchall()
print(rows)


### Create table departments

c.execute(''' drop table if exists departments ''')
c.execute(''' CREATE TABLE IF NOT EXISTS departments (
               dept_id INT  auto_increment,
               dept_name TEXT ,
               PRIMARY KEY(dept_id)

               ); ''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('admin')''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('sales')''')
c.execute(''' INSERT INTO departments(dept_name)
                VALUES ('development')''')
 
##### Fetch all data from departments 
c.execute("SELECT * FROM departments ")
rows = c.fetchall()
print(rows)


#Create table user_profile
c.execute (''' drop table if exists userprofile ''')
c.execute (''' CREATE TABLE IF NOT EXISTS userprofile (
                user_id INT auto_increment ,
                prof_name TEXT ,
                is_admin INT ,
                PRIMARY KEY (user_id)
            
                ); ''')
c.execute(''' INSERT INTO userprofile(prof_name,is_admin)
                VALUES ('Manager',1)''')
c.execute(''' INSERT INTO userprofile(prof_name,is_admin)
                VALUES ('Sales',0)''')
c.execute(''' INSERT INTO userprofile(prof_name,is_admin)
                VALUES ('Developer',0)''')

###Fetch all data from userprofile
c.execute("SELECT * FROM userprofile")
rows = c.fetchall()
print(rows)



## Add foreign key
c.execute(''' ALTER TABLE users
            ADD FOREIGN KEY (user_id) REFERENCES userprofile(user_id) ON UPDATE CASCADE ; ''')
c.execute(''' ALTER TABLE users
            ADD FOREIGN KEY (dept_id) REFERENCES departments (dept_id) ON UPDATE CASCADE ; ''' )



#fetch data in dataframe
c.execute("SELECT * FROM users")
rows= c.fetchall()
df = pd.DataFrame(rows)
print(df)

#show table:
c.execute("SHOW TABLES")
for x in c :
    print(x)

test.close()
