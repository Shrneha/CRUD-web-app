from flask import Flask, render_template, request  #request object to get value of zip
from flask_mysqldb import MySQL
import mysql.connector
import os.path
from os import path
import pandas as pd

app = Flask(__name__)

def create_database():
    test = mysql.connector.connect(
        host     = "localhost" ,
        user     = "admin"     ,
        passwd   = "admin"
        )
    c = test.cursor()
    # Create table 'cdr'
    c.execute(''' CREATE DATABASE test ''')
    c.execute(''' USE test ''')
    c.execute(''' CREATE TABLE IF NOT EXISTS cdr(
          id INT PRIMARY KEY,
          date DATE         ,
          time TIME         ,
          extno INT         ,
          extnm TEXT        ,
          trkno INT         ,
          trknm TEXT        ,
          clidno INT        ,
          clidnm TEXT       ,
          phonno INT        ,
          phonnonm TEXT     ,
          calldurn INT      ,
          ringdurn INT      ,
          calldir TEXT
          ) ;
          ''')
    print("Database 'test' created successfully.")

def connect_db() :
    try: 
        test = mysql.connector.connect(
        host     = "localhost" ,
        user     = "admin"     ,
        passwd   = "admin"     ,
        database = "test"
        )
        c = test.cursor()

        # Create table 'cdr'
        c.execute(''' CREATE TABLE IF NOT EXISTS cdr(
          id INT PRIMARY KEY,
          date DATE         ,
          time TIME         ,
          extno INT         ,
          extnm TEXT        ,
          trkno INT         ,
          trknm TEXT        ,
          clidno INT        ,
          clidnm TEXT       ,
          phonno INT        ,
          phonnonm TEXT     ,
          calldurn INT      ,
          ringdurn INT      ,
          calldir TEXT
          ) ;
          ''')
        print("Database exists. CDR table created successfully")
    
    except :
        print("Database does not exist")
        create_database()

def check_raw_file(date):
    print ("File exists:"+str(path.exists('E:/tmp/%s.ra0' % date)))

def process_raw_file(date) :
    file=open("E:/tmp/%s.ra0" % date,"r")
    text= []
    for line in file :
        line= line.split()
        text.append(line)
        
    with open("C:/Users/admin/Desktop/New folder/output.txt", "w") as f:
        for line in text :
            print(line , sep=',', file=f)
        f.close()
        
    
connect_db() 
check_raw_file(20190730)
process_raw_file(20190730)

        
@app.route('/' , methods = ["GET","POST"])
def index():
    return render_template("get_date.html")

@app.route('/date' , methods = ["POST"])
def process():
    # Get user input
    start_date = request.form["stdate"]
    end_date = request.form["endate"]
    time = ""

    while start_date < end_date:
        file1=open("C:/Users/admin/Desktop/New folder/%s.cdr" % start_date,"r")
        # Process files 
        abc= []
        for line in file1 :
            line= line.split("|")
            abc.append(line)
        start_date= start_date +1
        
    file2=open("C:/Users/admin/Desktop/New folder/%s.cdr" % end_date,"r")
    for line in file2 :
        line= line.split("|")
        abc.append(line)
        
    with open("C:/Users/admin/Desktop/New folder/output.txt", "w") as f:
        for line in abc :
            print(line[2],line[4],line[8],line[10],line[12],line[22], sep=',', file=f)
        f.close()

    # Generate Excel File
    read_file = pd.read_csv(r'C:/Users/admin/Desktop/New folder/output.txt',encoding= 'unicode_escape')
    read_file.columns = ['Date','Time','EXT','Trunk','Name','CLI']
    read_file.to_csv(r'C:/Users/admin/Desktop/New folder/outputt.csv', index=None)
    return render_template("enter.html" , date= start_date)


if __name__ == '__main__' :
    app.run(debug=True) 
