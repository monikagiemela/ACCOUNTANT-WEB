from datetime import date, datetime
from flask import request, render_template, session
from app import app
from app.models import Accountants, History
from app.UTILS.helpers import login_required


@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """Show history of transactions"""
    
    accountant_id = session.get("accountant_id")
    accountant = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountant.current_balance

    # Fetche all transactions from table "History"
    transactions = History.query.filter_by(accountant_id=accountant_id).all()
    try:
        min_date = transactions[0].time
        max_date = transactions[-1].time
    except IndexError:
        context = {
        "current_balance": current_balance,
        "transactions": transactions
        }
    else:
        context = {
            "current_balance": current_balance,
            "transactions": transactions,
            "min_date": min_date,
            "max_date": max_date
        }

    if request.method == "GET":        
        return render_template("history.html", context=context)
    elif request.method == "POST":
        date_from = request.form.get("date_from")
        date_to = request.form.get("date_to")
        
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        transactions = History.query.filter(History.accountant_id==accountant_id, History.time >= date_from, History.time <= date_to).all()
        context = {
            "current_balance": current_balance,
            "transactions": transactions,
            "min_date": min_date,
            "max_date": max_date
        }
        return render_template("history.html", context=context)