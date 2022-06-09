from flask import render_template, session

from app import app
from app.models import Users, Accountants, Storage
from app.UTILS.helpers import login_required

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show storage details"""
    id = session.get("user_id")
    accountant_id = session.get("accountant_id")
    # Fetches available cash from table "Accountants"
    accountat = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountat.current_balance

    # Fetches all products in the storage
    storage = Storage.query.filter_by(accountant_id=accountant_id).all()
    context = {
        "storage": storage,
        "current_balance": current_balance
    }
    return render_template("index.html", context=context)