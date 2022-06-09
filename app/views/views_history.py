from flask import render_template, session
from app import app
from app.models import Accountants, History
from app.UTILS.helpers import login_required


@app.route("/history", methods=["GET"])
@login_required
def history():
    """Show history of transactions"""
    accountant_id = session.get("accountant_id")
    accountant = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountant.current_balance
              
    # Fetche all transactions from table "History"
    transactions = History.query.filter_by(accountant_id=accountant_id).all()
    context = {
        "current_balance": current_balance,
        "transactions": transactions
    }
    return render_template("history.html", context=context)