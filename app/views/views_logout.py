from flask import flash, redirect, session
from app import app


@app.route("/logout")
def logout():
    """Log user out"""
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    flash("You were successfully logged out")
    return redirect("/")