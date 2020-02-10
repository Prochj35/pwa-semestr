import os

from flask import Flask, flash, redirect, render_template, request, session, abort
from flask_socketio import SocketIO

import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "asdfasjdfdksj12432#"
socketio = SocketIO(app)

engine = create_engine('sqlite:///users.db', echo=True)

user_session_ids = dict()
user_session_name = ''


@app.route('/registration', methods=['POST'])
def add_user():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]))
    result = query.first()

    if result:
        flash("This username is already taken!")
    else:
        user = User(POST_USERNAME, POST_PASSWORD)    
        s.add(user)
        s.commit()

    return home()


@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template("login.html")
    else:
        return sessions()


@app.route('/new')
def render_registration_form():
    return render_template("register.html")


@app.route('/chat')
def sessions():
    print("active users: " + str(user_session_ids))
    return render_template("/production/plain_page.html", active_users = user_session_ids, username = user_session_name)
#    return render_template("chat-old.html", active_users = user_session_ids)


@socketio.on('login')
def store_session_id(username):
    print(username + ":" + request.sid)
    user_session_ids[username] = request.sid
    user=[username, request.sid]
    socketio.emit("user_connected", user)
    return home()


@socketio.on('private_chat')
def create_private_chat(data):
    user_from = data["from"]
    user_to = data["to"]
    print("private chat: " + user_from + " and " + user_to)
    print("user_to id: " + user_session_ids[user_to])
    socketio.emit("create_chat", {"u_from": user_from, "u_to": user_to})


@socketio.on('private_message')
def handle_private_message(data):
    user_from = data["user_name"]
    user_to = data["user_to"]
    message = data["message"]
    print("from: " + user_from + " to: " + user_to + " - " + message)
    socketio.emit("handle_pm", {"from":user_from, "to":user_to, "message":message})


@app.route('/login', methods=['POST'])
def process_login():
    POST_USERNAME = str(request.form['username'])
    user_session_name = POST_USERNAME
    POST_PASSWORD = str(request.form['password'])
 
    Session = sessionmaker(bind=engine)
    s = Session()
    query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
    result = query.first()

    if result:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return home()

def message_received(methods=['GET', 'POST']):
    print("Message was received")

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print("Received my event: " + str(json))
    socketio.emit("my response", json, callback=message_received)

@socketio.on("user_logout")
def handle_user_logout(user):
    print("Received: " + str(user["data"]))
    user_session_ids.pop(str(user["data"]))
    socketio.emit("user_loggedout", str(user["data"]))

if __name__ == "__main__":
    from os import environ
    socketio.run(app, debug=False, host="0.0.0.0", port=environ.get("PORT", 5000))
