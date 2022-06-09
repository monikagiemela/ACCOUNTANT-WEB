from flask import flash, redirect, render_template, request, session
from werkzeug.security import check_password_hash

from app import app
from app.models import Users
from app.UTILS.helpers import apology


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("email_address"):
            return apology("Email address is required", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Password is required", 400)

        # Query database for email_address and check password  
        try:
            user = Users.query.filter_by(email_address=request.form.get("email_address")).first()
        except AttributeError:
            return apology("Invalid email address", 400)
            
        try:
            check_password_hash(user.hash, request.form.get("password"))
        except:
            return apology("Invalid password", 400)

        # Remember which user has logged in
        session["user_id"] = user.id
        session["accountant_id"] = user.accountant_id
        flash('You were successfully logged in')
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")