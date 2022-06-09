from flask import request, render_template, session
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
    try:
        min_date = transactions[0].time.date()
        max_date = transactions[-1].time.date()
    except IndexError:
        context = {
        "current_balance": current_balance,
        "transactions": transactions,
    }
    else:
        context = {
            "current_balance": current_balance,
            "transactions": transactions,
            min_date: min_date,
            max_date: max_date
        }
    return render_template("history.html", context=context)

@app.route("/history/<date_from>/<date_to>", methods=["GET"])
@login_required
def history_specify(date_from, date_to):
    """Show history of transactions for given dates"""
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")
    accountant_id = session.get("accountant_id")
    accountant = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountant.current_balance
    print(date_from)
    print(date_to)   
    # Fetche all transactions from table "History"
    transactions = History.query.filter_by(accountant_id=accountant_id).all()
    context = {
        "current_balance": current_balance,
        "transactions": transactions,
    }
    return render_template("history.html", context=context)