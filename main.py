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

## List table rows
@app.route('/session/emp',methods=['GET','POST'])
def list_employees():
    username = session["username"]
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT users.username ,userprofile.is_admin
                                  FROM users
                                  LEFT JOIN userprofile ON users.user_id = userprofile.user_id
                                  WHERE username = %s ''',(username,))
    result = cur.fetchone()
    if result[1] == 1 :
        cur.execute("SELECT * FROM users")
        result = cur.fetchall()
        cur.close()
        return render_template('admin_employees.html', users=result, username = username)
    else :
        cur.execute ("SELECT * FROM users where username = %s",(username,))
        result = cur.fetchall()
        cur.close()
        return render_template('employees.html', users=result, username = username)\

@app.route('/session/dept',methods =['GET','POST'])
def list_dept():
    username = session["username"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM departments")
    result = cur.fetchall()
    cur.close()
    return render_template('admin_dept.html',users = result ,username = username)

@app.route('/session/userprofile',methods =['GET','POST'])
def list_userprofile():
    username = session["username"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM userprofile")
    result = cur.fetchall()
    cur.close()
    return render_template('admin_userprofile.html',users = result ,username = username)


## Update table rows
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

@app.route('/dept_update',methods = ['POST'])
def dept_update():
    dept_id = request.form['dept_id']
    dept_name = request.form['dept_name']
    cur = mysql.connection.cursor()
    cur.execute(''' UPDATE departments
                    SET dept_id = %s , dept_name =%s WHERE dept_id =%s ''',(dept_id,dept_name,dept_id,))
    mysql.connection.commit()
    return redirect(url_for('list_dept'))

@app.route('/userprofile_update',methods = ['POST'])
def userprofile_update():
    user_id = request.form['user_id']
    prof_name = request.form['prof_name']
    is_admin = request.form['is_admin']
    cur = mysql.connection.cursor()
    cur.execute(''' UPDATE userprofile
                    SET user_id = %s , prof_name =%s , is_admin=%s WHERE user_id =%s ''',(user_id,prof_name,is_admin,user_id,))
    mysql.connection.commit()
    return redirect(url_for('list_userprofile'))


## Delete table rows 
@app.route('/delete/<string:id_data>', methods=["GET"])
def delete(id_data):
    cur = mysql.connection.cursor()
    cur.execute(" DELETE FROM users WHERE id= %s ", (id_data,))
    mysql.connection.commit()
    return redirect(url_for('list_employees'))

@app.route('/delete_dept/<string:dept_id>', methods=["GET"])
def delete_dept(dept_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM departments WHERE dept_id = %s", (dept_id,))
    mysql.connection.commit()
    return redirect(url_for('list_dept'))

@app.route('/delete_userprofile/<string:user_id>', methods=["GET"])
def delete_userprof(user_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM userprofile WHERE user_id = %s ", (user_id,))
    mysql.connection.commit()
    return redirect(url_for('list_userprofile'))



## add users 
@app.route('/add_user',methods =["POST"])
def add_user():
    username = session["username"]
    cur = mysql.connection.cursor()
    cur.execute(''' SELECT users.username ,userprofile.is_admin
                                  FROM users
                                  LEFT JOIN userprofile ON users.user_id = userprofile.user_id
                                  WHERE username = %s ''',(username,))
    result = cur.fetchone()
    if result[1] == 1 :
        username = request.form['username']
        password = request.form['password']
        dept_id = request.form['dept_id']
        user_id = request.form['user_id']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username,password,dept_id,user_id) VALUES (%s,%s,%s,%s)",(username,password,dept_id,user_id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('list_employees'))
    else :
        return redirect(url_for('list_employees'))

@app.route('/add_dept',methods=['POST'])
def add_dept():
    dept_id = request.form["dept_id"]
    dept_name = request.form["dept_name"]
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO departments (dept_id,dept_name) VALUES (%s,%s)",(dept_id,dept_name))
    mysql.connection.commit()
    return redirect(url_for('list_dept'))

@app.route('/add_userprofile',methods=['POST'])
def add_userprofile():
    user_id = request.form["user_id"]
    prof_name = request.form["prof_name"]
    is_admin = request.form["is_admin"]
    cur = mysql.connection.cursor()
    cur.execute(" INSERT INTO userprofile (user_id,prof_name,is_admin) VALUES (%s,%s,%s)",(user_id,prof_name,is_admin))
    mysql.connection.commit()
    return redirect(url_for('list_userprofile'))



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
                    c.execute(''' SELECT users.username ,userprofile.is_admin
                                  FROM users
                                  LEFT JOIN userprofile ON users.user_id = userprofile.user_id
                                  WHERE username = %s ''', (username,))
                    result = c.fetchone()
                    if result[1] == 1 :
                        return render_template("admin_logged_in.html", username = username) 
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
        return render_template("logged_in.html" ,username = username)
    else:
        return render_template('index1.html')
    

@app.route('/logout',methods=['POST','GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))




if __name__ == '__main__':
    app.run(debug= True)
