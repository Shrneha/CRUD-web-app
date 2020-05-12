
from flask import Flask
import sqlite3 as sql
from flask import render_template ,request ,flash
import sqlite3
con = sql.connect('users.db')
c =  con.cursor()

app = Flask(__name__)
#app.secret_key = "super secret key"

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
                    #flash("Invalid Credentials")
                    return render_template('index1.html')
            
if __name__ == '__main__' :
    app.run(debug=True )

                
            
                      
                      
            
##        completion = validate(username, password)
##        if completion ==False:
##            error = 'Invalid Credentials. Please try again.'
##        else:
##            return redirect(url_for('secret'))
##    return render_template('index1.html', error=error)

##def validate(username, password):
##    con = sqlite3.connect('users.db')
##    completion = False
##    with con:
##                cur = con.cursor()
##                cur.execute("SELECT * FROM users")
##                rows = cur.fetchall()
##                for row in rows:
##                    dbUser = row[0]
##                    dbPass = row[1]
##                    if dbUser==username:
##                        completion=check_password(dbPass, password)
##    return completion

##def login():
##    username = request.form["username"]
##    password = request.form["password"]
##    
##def login():
##    if form.validate():
##        username= request.form['username']
##        password= request.form['password']
##        auth = c.execute("SELECT username FROM users WHERE username = (?)",(username))
##        user_exists = auth.fetchone()
##        if user_exists:
##            auth = c.execute("SELECT password FROM users WHERE password = (?)",(password))
##            password_correct = auth.fetchone()
##            if password_correct:
##                print("Logged In")
##                return redirect(url_for('home'))
##            else :
##                return 'Incorrect attempt'
##        else :
##            return 'Incorrect Attempt'
##    return render_template('index1.html')

