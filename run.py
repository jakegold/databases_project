#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
from time import localtime, strftime
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)
app.secret_key = 'a super secret key'

#Configure MySQL
conn = pymysql.connect(host='localhost',
		       user='root',
		       password='',
		       db='pricosha',
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
	first_name = request.form['first_name']
	last_name = request.form['last_name']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM person WHERE username = %s'
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
		ins = 'INSERT INTO person (username, password, first_name, last_name) VALUES(%s, MD5(%s), %s, %s)'
		cursor.execute(ins, (username, password, first_name, last_name))
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
def home(error = None):
	username = session['username']
	if error:
		return render_template('home.html', username=username, error = error)
	return render_template('home.html', username=username)

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

@app.route('/user_content')
def user_content():
	user = session['username']
	cursor = conn.cursor();
	query = 'SELECT * FROM content WHERE content.username = %s OR public = TRUE OR content.id IN (SELECT id FROM share WHERE group_name IN (SELECT group_name FROM member WHERE username = %s)) ORDER BY content.timest DESC'
	cursor.execute(query, (user,user))
	data = cursor.fetchall()
	session['data'] = data
	return render_template('content.html', username = user, posts=data)

@app.route('/content_info', methods=['GET', 'POST'])
def content_info():
	user = session['username']
	cursor = conn.cursor();
	data = session['data']
	content = request.form["view content"]
	tag_query = 'SELECT username_tagger, username_taggee FROM `tag` WHERE status = true AND id = %s'
	comment_query = 'SELECT * FROM comment WHERE id =%s'
	cursor.execute(tag_query, (content))
	tag_data = cursor.fetchall()
	cursor.execute(comment_query, (content))
	comment_data = cursor.fetchall()
	return render_template('content.html', username = user, posts=data, tags = tag_data, comments = comment_data)

@app.route('/post_user_content')
def render_post_content():
	return render_template('post_content.html')

@app.route('/post_user_content', methods=['POST'])
def post_content_pub():
	user = session['username']
	cursor = conn.cursor()
	title = request.form['title']
	link = request.form['link']
	is_pub = request.form['Make Public']
	pub = 0
	if is_pub == 'yes':
		pub = 1
	post_query = 'INSERT INTO content (id, username, timest, file_path, content_name, public) VALUES (NULL, %s, CURRENT_TIME(), %s, %s, %s)'
	cursor.execute(post_query, (user,link,title,pub))
	conn.commit()
	if pub:
		return redirect(url_for('home'))
	else:
		query = 'SELECT * FROM friendgroup WHERE username = %s'
		cursor.execute(query,(user))
		data = cursor.fetchall()
		session['friendgroups'] = data
		return render_template('post_content_group.html', groups = data)

@app.route('/post_content_group', methods=['GET', 'POST'])
def post_content_group():
	user = session['username']
	cursor = conn.cursor()
	fg = request.form['group name']
	id_query = 'SELECT id FROM content ORDER BY id DESC LIMIT 1'
	cursor.execute(id_query)
	content_id = cursor.fetchone()
	content_id = content_id['id']
	query = 'SELECT * FROM friendgroup WHERE username = %s AND group_name = %s'
	cursor.execute(query,(user, fg))
	data = cursor.fetchone()
	groups = session['friendgroups']
	if not data:
		error = "That is not a friend group you can add to"
		return render_template('post_content_group.html', error = error, groups = groups)
	query2 = 'SELECT * FROM share WHERE username = %s AND id = %s AND group_name = %s'
	cursor.execute(query2, (user, content_id, fg))
	data2 = cursor.fetchone()
	if data2:
		error = "You've already posted that content to that group!"
		return render_template('post_content_group.html', error = error, groups = groups)
		
	query = "INSERT INTO share (id, group_name, username) VALUES (%s, %s,%s)"
	cursor.execute(query, (content_id, fg,user))
	conn.commit()
	return render_template('post_content_group.html', groups = groups)
	
#Define route for adding a friend
@app.route('/addFriend')
def addFriend():
	return render_template('addFriend.html')

#Authenticates the addition
@app.route('/addFriendAuth', methods=['GET', 'POST'])
def addFriendAuth():
        username = session['username']
        friendGroup = request.form['friendGroup'] 
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cursor = conn.cursor()

        #getting username of friend to add
        query = 'SELECT username FROM person WHERE first_name = %s AND last_name = %s'
        cursor.execute(query, (firstname, lastname))
        data = cursor.fetchall()
        error = None

        #if more than one username is found under the same name, the user is directed to the Add Friend By Username page
        if len(data) > 1: 
                return render_template('addFriendU.html')

	#checks if the friend is already in the friendgrou
        query = 'SELECT * FROM member WHERE username = (SELECT username FROM person WHERE first_name = %s AND last_name = %s) AND group_name = %s AND username_creator = %s' 
        cursor.execute(query, (firstname, lastname, friendGroup, username))
        data = cursor.fetchone()
        #if the friend is already in the group, redirects to add friend page
        if(data):
                error = "This user already exists in this friend group- please try again:"
                return render_template('addFriend.html', error = error)

        else:
                added_user = 'SELECT username FROM person WHERE first_name = %s AND last_name = %s'
                cursor.execute(added_user, (firstname, lastname))
                new_user = cursor.fetchone()
                new_user = new_user['username']

                ins = 'INSERT INTO member (group_name, username, username_creator) VALUES (%s, %s, %s)'
                cursor.execute(ins, (friendGroup, new_user, username))
                conn.commit()
                return render_template('home.html')

#Define route for adding a friend
@app.route('/addFriendU')
def addFriendU():
	return render_template('addFriendU.html')

#Authenticates the addition
@app.route('/addFriendAuthU', methods=['GET', 'POST'])
def addFriendAuthU():
	username = session['username']
	friendGroup = request.form['friendGroup'] 
	friendName = request.form['friendUsername']
	cursor = conn.cursor()
	query = 'SELECT * FROM member WHERE username = %s AND group_name = %s AND username_creator = %s' 
	cursor.execute(query, (friendName, friendGroup, username))
	data = cursor.fetchone()

	if(data):
		error = "This user already exists in this friend group"
		return render_template('addFriendU.html', error = error)
	else:
		ins = 'INSERT INTO member (group_name, username, username_creator) VALUES (%s, %s, %s)'
		cursor.execute(ins, (friendGroup, friendName, username))
		conn.commit()
		cursor.close()
		return render_template('home.html')

@app.route('/tag_content', methods=['GET', 'POST'])
def tag_content():
	#handles: person doesnt exist, person not in a group with this item,
	#Doesn't handle, a person trying to tag someone twice, should I do that? Probably. I will if I remember to.
	username = session['username']
	cursor = conn.cursor()
	content_id = request.form['content_id']
	friend = request.form['friend_username']
	pubq = 'SELECT public FROM content WHERE id = %s'
	cursor.execute(pubq, (content_id))
	is_pub = cursor.fetchone()
	is_pub = is_pub['public']
	if username != friend: #Not self tagging
		if is_pub: #if it is public then we don't need to worry about the group, just that the person exists
			q2 = 'SELECT * FROM person WHERE username = %s'
			cursor.execute(q2, friend)
			data = cursor.fetchone()
		else:
			inGroupq = 'SELECT username FROM member WHERE username = %s AND group_name IN (SELECT group_name FROM share WHERE id = %s)'
			cursor.execute(inGroupq, (friend, content_id))
			data = cursor.fetchone()
			
		if(data): #does this person exist in the group
			query = 'INSERT INTO tag (id, username_tagger, username_taggee, timest, status) VALUES (%s, %s, %s, CURRENT_TIME(), 0)'
			cursor.execute(query, (content_id, username, friend))
			conn.commit()
			cursor.close()
		else:
			error = "This person either does not exist or does not belong to a group with this content"
			return home(error)               
	else:#self-tagging
		query = 'INSERT INTO tag (id, username_tagger, username_taggee, timest, status) VALUES (%s, %s, %s, CURRENT_TIME(), 1)'
		cursor.execute(query, (content_id, username, friend))
		conn.commit()
		cursor.close()
	return redirect(url_for('home'))

@app.route('/manage_tags', methods=['GET', 'POST'])
def manage_tags():
	user = session['username']
	cursor = conn.cursor()
	tag_query = 'SELECT * FROM tag JOIN content ON tag.id = content.id WHERE username_taggee = %s AND status = 0'
	cursor.execute(tag_query, (user))
	tag_data = cursor.fetchall()
	return render_template('manageTags.html', tags = tag_data)

@app.route('/approve_tag', methods=['GET', 'POST'])
def approve_tag():
	user = session['username']
	cursor = conn.cursor()
	content_id = request.form['id']
	tagger = request.form['tagger']
	query = 'UPDATE tag SET status = 1 WHERE id = %s AND username_taggee = %s AND username_tagger = %s'
	cursor.execute(query, (content_id, user, tagger))
	conn.commit()
	cursor.close()
	return redirect(url_for('manage_tags'))

@app.route('/reject_tag', methods=['GET', 'POST'])
def reject_tag():
	user = session['username']
	cursor = conn.cursor()
	content_id = request.form['id']
	tagger = request.form['tagger'] 
	query = 'DELETE FROM tag WHERE id = %s AND username_taggee = %s AND username_tagger = %s'
	cursor.execute(query, (content_id, user, tagger))
	conn.commit()
	cursor.close()
	return redirect(url_for('manage_tags'))

		
if __name__ == "__main__":
	app.run('127.0.0.1', 5001, debug = True)


