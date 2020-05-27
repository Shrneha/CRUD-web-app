from flask import Flask
from flask import render_template ,request ,flash,session,redirect,url_for
from flask_mysqldb import MySQL
from flask_table import Table,Col
import pymysql


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'test'
app.config['MYSQL_DATABASE_PORT']= '3306'
app.config['SECRET_KEY'] = "My Super Secret Key"
mysql = MySQL(app)

@app.route('/session/emp',methods=['GET','POST'])
def list_employees():
    username = session["username"]
    cur = mysql.connection.cursor()
    if 'admin' in username :
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        cur.close()
        return render_template('employees.html', users=result, username = username)
    else :
        cur.execute("SELECT * FROM users where username = %s",(username,) )
        result = cur.fetchall()
        cur.close()
        return render_template('employees.html', users=result, username = username)


@app.route('/update', methods=["POST"])
def update():
    id_data = request.form['id']
    username = request.form['username']
    password = request.form['password']
    dept_id = request.form['dept_id']
    user_id = request.form['user_id']
    cur = mysql.connection.cursor()
    cur.execute('''UPDATE users
                SET username=%s,password=%s, dept_id=%s ,user_id=%s
                WHERE id=%s''', (username,password,dept_id,user_id, id_data,))
    mysql.connection.commit()
    return redirect(url_for('list_employees'))

@app.route('/delete/<string:id_data>', methods=["GET"])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM users WHERE id=%s", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('list_employees'))

@app.route('/add_user',methods =["POST"])
def add_user():
    username = request.form['username']
    password = request.form['password']
    dept_id = request.form['dept_id']
    user_id = request.form['user_id']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO users (username,password,dept_id,user_id) VALUES (%s,%s,%s,%s)",(username,password,dept_id,user_id))
    mysql.connection.commit()
    return redirect(url_for('list_employees'))


##@app.route('/update_emp', methods=['GET', 'POST'])
##def up():
##    username = session["username"]
##    return render_template('update_emp.html')

    
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
                    #return render_template("logged_in.html" ,username = username)   
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

