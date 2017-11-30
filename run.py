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
def home():
        username = session['username']
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

@app.route('/post_user_content')
def render_post_content():
        return render_template('post_content.html')

##@app.route('/post_user_content', methods=['POST'])
##def post_content():
##        user = session['username']
##        cursor = conn.cursor();
##        file_path = user + '_file_path'
##        content_name = user + '_content_name'
##
##        tag = request.form['tag'] 
##        if tag:
##                #THIS IS USED SOMEWHERE ELSE MAKE A DIFF FUNCTION AND CALL IT FOR BOTH OF THESE
##                person_query = 'SELECT * FROM person WHERE username = %s' 
##                cursor.execute(person_query, (tag))
##                is_person = cursor.fetchone()
##                if not is_person:
##                        error = "This is not a user!"
##                        return render_template('post_content.html', error = error)
##
##        query = 'INSERT INTO content (username, file_path, content_name, public) VALUES(%s, %s, %s, %s)'
##        cursor.execute(query, (user, file_path, content_name, True))
##
##        cur_time = strftime("%Y-%m-%d %H:%M", localtime())
##        cur_time = str(cur_time) + '%'
##
##        id_query = 'SELECT id from content where username=%s and timest like %s'
##        cursor.execute(id_query, (user, cur_time))
##        data = cursor.fetchone()
##        data = data['id']
##
##        comment = request.form['comment'] 
##        post_query = 'INSERT INTO comment (id, username, comment_text) VALUES(%s, %s, %s)'
##        cursor.execute(post_query, (data, user, comment))
##
##        if tag:
##                tag_query = 'INSERT into tag (id, username_tagger, username_taggee, status) values(%s, %s, %s, %s)'
##                cursor.execute(tag_query, (data, user, tag, True))              
##
##        conn.commit()
##        cursor.close()
##        return render_template('post_content.html')     

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
def post_content_priv():
        user = session['username']
        cursor = conn.cursor()
        fg = request.form['group name']
        id_query = 'SELECT id FROM content ORDER BY id DESC LIMIT 1'
        cursor.execute(id_query)
        content_id = cursor.fetchone()
        content_id = content_id['id']
        query = 'SELECT * FROM friendgroup WHERE username = %s'
        cursor.execute(query,(user))
        data = cursor.fetchall()
        not_in = 0
        data = session['friendgroups']
        for line in data:
                if line['group_name'] == fg:
                        not_in =1
        if not_in==0:
                error = "that is not a friend group you can add to"
                return render_template('post_content_group.html', error = error, groups = data)
        query = "INSERT INTO share (id, group_name, username) VALUES (%s, %s,%s)"
        cursor.execute(query, (content_id, fg,user))
        conn.commit()
        return render_template('post_content_group.html', groups = data)
        
@app.route('/tags', methods=['GET', 'POST'])
def tags():
        user = session['username']
        cursor = conn.cursor();
        data = session['data']
        content = request.form["view tags"]
        tag_query = 'SELECT username_tagger, username_taggee FROM `tag` WHERE status = true AND id = %s'
        comment_query = 'SELECT * FROM comment WHERE id =%s'
        cursor.execute(tag_query, (content))
        tag_data = cursor.fetchall()
        cursor.execute(comment_query, (content))
        comment_data = cursor.fetchall()
        return render_template('content.html', username = user, posts=data, tags = tag_data, comments = comment_data)

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
