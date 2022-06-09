import re

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

def login_required(f):
    """Decorate routes to require login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

def absolute(quantity):
    """Format value as absolute"""
    if quantity < 0:
        return quantity * (-1)
    return quantity

def validate_new_password(password, confirmation):
    """Validate format of the password entered by the user"""
    if not password or password != confirmation:
        return apology("Make sure that Password and Confirmation match", 400)
    if len(password) < 8:
        return apology("Make sure your password is at lest 8 characters", 400)
    if not re.search("[0-9]", password):
        return apology("Make sure your password has a number in it", 400)
    if not re.search("[A-Z]", password):
        return apology("Make sure your password has a capital letter in it", 400)
    if not re.search("[a-z]", password):
        return apology("Make sure your password has a lower-case letter in it", 400)
    if not re.search("[!@#$%^&*()-_]", password):
        return apology("Make sure your password has a special sign in it", 400)   