#===========================================================
# APP NAME HERE
# By YOUR NAME HERE
#===========================================================

from flask import Flask, request, session, render_template, flash, redirect, send_file, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from os import getenv
from io import BytesIO
import html
from app.helpers import *


# Create the app
app = Flask(__name__)


#===========================================================
# App Routes Handlers
#===========================================================

#-----------------------------------------------------------
# Signup page
#-----------------------------------------------------------
@app.get("/user/new")
def show_signup():
    return render_template("pages/user_signup.jinja")

#-----------------------------------------------------------
# Login page
#-----------------------------------------------------------
@app.get("/user/login")
def show_login():
    return render_template("pages/user_login.jinja")



#-----------------------------------------------------------
# Welcome page
#-----------------------------------------------------------
@app.get("/")
def show_welcome():
    return render_template("pages/welcome.jinja")


#-----------------------------------------------------------
# Message display page
#-----------------------------------------------------------
@login_required
@app.get("/messages")
def show_messages():
    with connect_db() as db:
        sql = "SELECT * FROM messages"
        messages = db.execute(sql).fetchall()
    return render_template("pages/messages_display.jinja", messages=messages)

#-----------------------------------------------------------
# New Message page
#-----------------------------------------------------------
@login_required
@app.get("/messages/new")
def show_new_message():
    return render_template("pages/messages_new.jinja")



#-----------------------------------------------------------
# Edit Message page
#-----------------------------------------------------------
@login_required
@app.get("/messages/edit/<int:id>")
def show_edit_message(id):


    with connect_db() as db:
        sql = "SELECT * FROM messages WHERE id=?"
        params = (id,)
        message = db.execute(sql, params).fetchone()

    # Only the owner/admin should be able to edit their own message
   
    posted_by = message["posted_by"]
    if (not is_owner_or_admin(posted_by)): 
        return redirect("/messages")

    return render_template("pages/messages_edit.jinja",message=message)


#-----------------------------------------------------------
# Handle New Message
#-----------------------------------------------------------
@login_required
@app.post("/messages/new")
def add_new_message():
    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()


    with connect_db() as db:
        sql = """INSERT INTO messages (title, body, posted_by)
                    VALUES (?,?,?)
            """
        params = (title, body, session["user"]["username"])
        message = db.execute(sql, params).fetchone()
    return redirect("/messages")


#-----------------------------------------------------------
# Handle Edit Message
#-----------------------------------------------------------
@login_required
@app.post("/messages/edit/<int:id>")
def process_edit_message(id):

    # Only the owner should be able to edit their own message
    with connect_db() as db:
        sql = "SELECT posted_by FROM messages WHERE id=?"
        params = (id,)
        posted_by = db.execute(sql, params).fetchone()["posted_by"]
    
    if ( not is_owner_or_admin(posted_by) ): 
        return redirect("/messages")


    title = request.form.get('title', '').strip()
    body = request.form.get('body', '').strip()


    with connect_db() as db:
        sql = """UPDATE messages SET title = ?, body = ? WHERE id = ?
            """
        params = (title, body, id)
        message = db.execute(sql, params).fetchone()
    return redirect("/messages")


#-----------------------------------------------------------
# Handle Delete Message
#-----------------------------------------------------------
@login_required
@app.get("/messages/delete/<int:id>")
def process_delete_message(id):

    # Only the owner or admin should be able to delete their own message
    with connect_db() as db:
        sql = "SELECT posted_by FROM messages WHERE id=?"
        params = (id,)
        posted_by = db.execute(sql, params).fetchone()["posted_by"]
    
    if (not is_owner_or_admin(posted_by)): 
        return redirect("/messages")

    with connect_db() as db:
        sql = """DELETE FROM messages WHERE id = ?
            """
        params = (id,)
        result = db.execute(sql, params)
    return redirect("/messages")



#-----------------------------------------------------------
# Handle new user
#-----------------------------------------------------------
@app.post("/user")
def process_new_user():

    forename = request.form.get('forename', '').strip()
    surname  = request.form.get('surname',  '').strip()
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = "SELECT username FROM users WHERE username=?"
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if user:
            flash(f"Username '{username}' already exists", "error")
            return redirect("/user/new")

        pass_hash = generate_password_hash(password)

        sql = """
            INSERT INTO users (username, password_hash, forename, surname)
            VALUES (?, ?, ?, ?)
        """
        params = (username, pass_hash, forename, surname)
        db.execute(sql, params)

        flash("Account created. Please login", "success")
        return redirect("/user/login")


#-----------------------------------------------------------
# Handle Login Request
#-----------------------------------------------------------
@app.post("/user/login")
def login_user():
    username = request.form.get('username', '').strip().lower()
    password = request.form.get('password', '').strip()

    with connect_db() as db:
        sql = """
            SELECT username, password_hash, forename, surname, is_admin
            FROM users
            WHERE username=?
        """
        params = (username,)
        user = db.execute(sql, params).fetchone()

        if not user:
            flash(f"Unknown user", "error")
            return redirect("/user/login")

        if not check_password_hash(user["password_hash"], password):
            flash(f"Incorrect password", "error")
            return redirect("/user/login")

        session["logged_in"] = True
        session["user"] = {
            "username": username,
            "forename": user["forename"],
            "surname":  user["surname"],
            "is_admin": user["is_admin"],
        }

        flash("Login successful", "success")
        return redirect("/")

#-----------------------------------------------------------
# Logout Past
#-----------------------------------------------------------
@app.get("/user/logout")
def logout():
    session.clear()
    flash(f"You have been logged out", "success")
    return redirect("/")



#===========================================================
# Configure the app
#===========================================================
load_dotenv()
app.config.from_prefixed_env()
init_logging(app)
init_text_filters(app)
init_date_filters(app)
init_error_handlers(app)
init_database()
register_commands(app)

