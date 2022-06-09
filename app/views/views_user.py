from flask import flash, render_template, request, session
from werkzeug.security import generate_password_hash
from app import app, db
from app.models import Users, Accountants, History
from app.UTILS.helpers import login_required, validate_new_password



@app.route("/user", methods=["GET", "POST"])
@login_required
def user():
    """Change user settings.
    Available options:
    - Deposit money
    - Withdraw money
    - Change  password"""
    id = session.get("user_id")
    accountant_id = session.get("accountant_id")
    user = Users.query.filter_by(id=id).first()
    accountant = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountant.current_balance
    if request.method == "GET":
        return render_template("user.html", current_balance=current_balance)
    elif request.method == "POST":
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        amount = request.form.get("amount")
        transaction = request.form.get("transaction")
        
        # If user entered a new password the following checks if user entered a valid format of a password
        if password:
            validate_new_password(password, confirmation)    
            # Update database
            user.hash = generate_password_hash(password, method="pbkdf2:sha256", salt_length=8)
            db.session.commit() 
            flash("You have successfuly changed your password")
            return render_template("user.html")
        # If user chose to deposit money
        elif amount:            
            amount = float(amount)
            if transaction == "deposit":
                current_balance += amount
                accountant.current_balance = current_balance
                new_transaction = History(transaction=transaction, value=amount, accountant_id=accountant_id, user_id=id)
                db.session.add(new_transaction)
                db.session.commit() 
                flash(f"You have successfuly deposited ${amount} to the Accountant")
                return render_template("user.html", current_balance=current_balance)
            # If user chose to withdraw money
            elif transaction == "withdraw":
                current_balance -= amount
                accountant.current_balance = current_balance
                new_transaction = History(transaction=transaction, value=amount, accountant_id=accountant_id, user_id=id)
                db.session.add(new_transaction)
                db.session.commit() 
                flash(f"You have successfuly withdrawn ${amount} from the Accountant")
                return render_template("user.html", current_balance=current_balance)