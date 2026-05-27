#===========================================================
# Auth Related Functions
#===========================================================

from flask import redirect, session, flash
from functools import wraps


#-----------------------------------------------------------
# A decorator function to check user logged in
# - This is determined by a 'logged_in' value being present
#   in the session
#-----------------------------------------------------------
def login_required(func):
    @wraps(func)
    # Wrap a given function...
    def wrapper(*args, **kwargs):

        # Is the user logged in?
        if session.get('logged_in'):
            # Yes, so run function
            return func(*args, **kwargs)

        # No, so go to home page
        flash("You need to be logged in", "error")
        return redirect("/")

    return wrapper

#---------------------------------------------------------
# Helper to check if is owner or admin for messages 
#---------------------------------------------------------
def is_owner_or_admin(owner_username):
    if(owner_username==session["user"]["username"]):
        return True
    if(session["user"]["is_admin"]):
        return True

    #Neither 
    return False
