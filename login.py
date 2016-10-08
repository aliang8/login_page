from flask import Flask, render_template, request, session, url_for, redirect
import hashlib

app = Flask(__name__) 

USERS = 'data/users.csv'
app.secret_key = '\x94$\xc6,\\\xd6\xa1\x90\xb7\x0c\xfc\xde\xa4-\xb1\r*h\x89\xf5\xc9\xa8\xec\x7f\x94\xfe\xae\x19\x14\xe9\x8c\xa5'

def getUsers():
    d = open(USERS,'r')
    data = d.read().strip()
    d.close()
    data = data.split('\n')
    users = {}
    if data[0] == '':
        return users
    for line in data:
        line = line.split(',')
        users[line[0]] = line[1]
    return users

def signin(username,password):
    users = getUsers()
    hashpasz = hashlib.sha224(password).hexdigest()
    if username in users and users[username] == hashpasz:
        return True
    else:
        return False

def register(username,password):
    users = getUsers()

    if username in users:
        return 1
    elif len(username) < 3 and len(password) < 3:
        return 2
    elif len(password) < 3:
        return 3
    elif len(username) < 3:
        return 4
    elif not(username.isalnum()) or not(password.isalnum()):
        return 5
    else: 
        pasz = hashlib.sha224(password).hexdigest()
        d = open(USERS,'a')
        entry = username + ',' + pasz + '\n'
        d.write(entry)
        d.close()
        return 6

@app.route("/")
def home():
    if 'username' in session:
        return render_template('main.html', message = session['username'])
    return redirect(url_for('login'))

@app.route("/login/")
def login():
    return render_template('login.html')

@app.route("/authenticate/", methods = ['POST'])
def auth():
    user = request.form['user']
    pasz = request.form['pass']
    hashpasz = hashlib.sha224(request.form['pass']).hexdigest()
    status = register(user,pasz)
    if 'login' in request.form:
        if signin(user,pasz):
            session['username'] = user
            return redirect(url_for('home'))
        else:
            return render_template('login.html',
                                    message = 'Login failed')
    else:
        if status == 1:
            return render_template('login.html',
                                    message = 'Registration failed. User already exists')
        elif status == 2:
            return render_template('login.html',
                                    message = 'Registration failed. Username and password too short')
        elif status == 3:
            return render_template('login.html',
                                    message = 'Registration failed. Password too short')
        elif status == 4:
            return render_template('login.html',
                                    message = 'Registration failed. Username too short')
        elif status == 5:
            return render_template('login.html',
                                    message = 'Registration failed. Username or password is not alphanumeric')
        else:
            return render_template('login.html',
                                    message = 'Registration successful!!!')

@app.route("/logout/", methods = ['POST'])
def logout():
    if 'logout' in request.form:
        session.pop('username')
        return redirect(url_for('login'))

if __name__ == '__main__': 
    app.debug = True #save file, restart webserver
    app.run() 
