import email
from flask import flash, redirect, render_template, request
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import Users, Accountants
from app.UTILS.helpers import apology, validate_new_password
from app.UTILS.Exception import userError


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Register user
    If a given Accountant already exists only a user with a valid Accountant password
    will be able to create a new user account for this Accountat.
    """
    if request.method == "POST":
        accountant_id = request.form.get("accountant_id")
        accountant_password = request.form.get("accountant_password")
        email_address = request.form.get("email_address")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check if username and password are entered correctly
        if not email_address or not password or not confirmation or not accountant_password:
            return apology("Accountat Password, Email Address, Password and Password Confirmation are required", 400)
        
        validate_new_password(password, confirmation)
        
        if accountant_id:            
            user = Users.query.filter_by(email_address=email_address).first()
            if user:
                return apology("This user already exists", 400)
            accountant = Accountants.query.filter_by(id=accountant_id).first() 
            if not accountant:
                # Create a new Accountants object and new Users object
                new_accountant = Accountants(hash=generate_password_hash(accountant_password, method="pbkdf2:sha256", salt_length=8))
                db.session.add(new_accountant)
                db.session.commit()
                accountant_id = new_accountant.id
                new_user = Users(email_address=email_address, hash=generate_password_hash(password, method="pbkdf2:sha256", salt_length=8), accountant_id=accountant_id)
                db.session.add(new_user)
                db.session.commit()
                flash(f"Congratulations! Successfully registered a new Accountant with id: {accountant_id} and a new user")
                return redirect("/")
            
            # Create a new Users object
            if accountant.hash == generate_password_hash(accountant_password, method="pbkdf2:sha256", salt_length=8):
                new_user = Users(email_address=email_address, hash=generate_password_hash(password, method="pbkdf2:sha256", salt_length=8), accountant_id=accountant_id)
                db.session.add(new_user)
                db.session.commit()
                flash("Congratulations! You were successfully registered and signed up to your Accountant")
                return redirect("/")
            
        # Create a new Accountants object and new Users object
        new_accountant = Accountants(hash=generate_password_hash(accountant_password, method="pbkdf2:sha256", salt_length=8))
        db.session.add(new_accountant)
        db.session.commit()
        accountant_id = new_accountant.id
        new_user = Users(email_address=email_address, hash=generate_password_hash(password, method="pbkdf2:sha256", salt_length=8), accountant_id=accountant_id)
        db.session.add(new_user)
        db.session.commit()
        flash(f"Congratulations! Successfully registered a new Accountant with id: {accountant_id} and a new user")
        return redirect("/")
    else:
        return render_template("register.html")