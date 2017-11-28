#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
import hashlib
#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'a super secret key'

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
                       db='project',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
	return render_template('register.html')

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM user WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO user (username, password) VALUES(%s, MD5(%s))'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM person WHERE username = %s and password = MD5(%s)'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('home'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('login.html', error=error)

@app.route('/home')
def home():
	username = session['username']
	return render_template('home.html', username=username)

@app.route('/user_content', methods=['GET', 'POST'])
def user_content():
        user = session['username']
        cursor = conn.cursor();
        query = 'SELECT * FROM content WHERE content.username = %s OR public = TRUE OR content.id IN (SELECT id FROM share WHERE group_name IN (SELECT group_name FROM member WHERE username = %s)) ORDER BY content.timest DESC'
        cursor.execute(query, (user,user))
        data = cursor.fetchall()
        return render_template('content.html', username = user, posts=data)

@app.route('/movies')
def movies():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT title, release_year, rating FROM movie'
	cursor.execute(query,)
	data = cursor.fetchall()
	cursor.close()
	return render_template('movies.html', username=username, posts=data)

@app.route('/bands')
def bands():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT title FROM band'
	cursor.execute(query,)
	data = cursor.fetchall()
	cursor.close()
	return render_template('bands.html', username=username, posts=data)

@app.route('/albums')
def albums():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT title FROM album'
	cursor.execute(query,)
	data = cursor.fetchall()
	cursor.close()
	return render_template('albums.html', username=username, posts=data)

@app.route('/songs')
def songs():
	username = session['username']
	cursor = conn.cursor();
	query = 'SELECT title FROM song'
	cursor.execute(query,)
	data = cursor.fetchall()
	cursor.close()
	return render_template('songs.html', username=username, posts=data)

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')

@app.route('/create/FriendGroup')
def FriendGroup():
	return render_template('Create_FriendGroup.html')


@app.route('/create/FriendGroup', methods=['GET', 'POST'])
def create_FriendGroup():
    username = session['username']
    group_name = request.form['group_name']
    description = request.form['description']
    cursor = conn.cursor()
    query = 'SELECT * FROM FriendGroup WHERE username = %s AND group_name = %s'
    cursor.execute(query, (username, group_name))
    data = cursor.fetchone()
    error = None
    if(data):
        error = "This group already exists for you!"
        return render_template('Create_FriendGroup.html', error = error)
    else:
        ins = 'INSERT INTO FriendGroup (username, group_name, description) VALUES (%s, %s, %s)'
        cursor.execute(ins, (username, group_name, description))
        conn.commit()
        cursor.close()
        return render_template('Create_FriendGroup.html', msg="Friend Group Created")



if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
