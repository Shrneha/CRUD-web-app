from flask import Flask
from flask import render_template ,request ,flash,session,redirect,url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_DATABASE_PORT']= '3306'
app.config['SECRET_KEY'] = "My Super Secret Key"
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index1.html')

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        c = mysql.connection.cursor()
        with c:
            c.execute('''SELECT * FROM users WHERE username = %s ''',[username])
            mysql.connection.commit()
            rows = c.fetchone()
            if rows != None:
                if rows[1] == username and rows[2] == password :
                    session['username'] = username
                    return redirect(url_for('sess'))
                        
                else :
                    flash("Plese enter correct password")
                    return render_template('index1.html')        
            else :
                flash("Invalid Username")
                return render_template('index1.html')

@app.route('/session')
def sess():
    if "username" in session:
        username = session["username"]
        #return f"<h3>You are logged in as {username}</h3>"
        return render_template("logged_in.html" ,username = username)
    else:
        return render_template('index1.html')
                
@app.route('/sign',methods = ['GET','POST'])
def sign():
    return render_template("signup.html")

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repassword = request.form['repassword']
        c = mysql.connection.cursor()
        with c:
            c.execute(''' SELECT * FROM users WHERE username LIKE (?) ''',( username,))
            mysql.connection.commit()
            row = c.fetchone()
            if row == None :
                if password == repassword :
                    c.execute('''INSERT INTO users (username ,password) VALUES (?,?)''',(username,password))
                    return render_template("index1.html")
                else :
                    flash("Password does not match ")
                    return render_template('signup.html')
            else :
                flash ("Username already exists")
                return render_template('signup.html')


@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
