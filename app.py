
from flask import Flask
import sqlite3 as sql
from flask import render_template ,request ,flash
import sqlite3
con = sql.connect('users.db')
c =  con.cursor()

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def home():
    return render_template('index1.html')

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    response = False
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        con = sql.connect('users.db')
        with con:
            c = con.cursor()
            c.execute("SELECT * FROM users")
            rows = c.fetchall()
            for row in rows :
                user = row[1]
                pwd = row[2]
                if user == username and pwd == password :
                    return render_template('logged_in.html')
                else :
                    return render_template('index1.html')
            
if __name__ == '__main__' :
    app.run(debug=True )

                
            
                      
                      
