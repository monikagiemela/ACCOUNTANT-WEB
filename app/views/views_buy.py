from flask import flash, redirect, render_template, request, session

from app import app, db
from app.models import Users, Accountants, History, Storage
from app.UTILS.helpers import apology, login_required


@app.route("/buy", methods=["POST", "GET"])
@login_required
def buy():
    """Buy shares of stock"""
    accountant_id = session.get("accountant_id")
    accountant = Accountants.query.filter_by(id=accountant_id).first()
    current_balance = accountant.current_balance
    if request.method == "POST":
        id = session.get("user_id")
        try: 
            product_name = request.form.get("product_name").lower()
        except:
            return apology("Enter product name", 400)
        try:
            quantity = float(request.form.get("quantity"))
        except:
            return apology("Enter product quantity")    
        try:
            price = float(request.form.get("price"))
        except:
            return apology("Enter purchase price per unit")
        try:
            sale_price = float(request.form.get("sale_price"))
        except:
            return apology("Enter sale price per unit")
        
        # Check if accountant has enough crediit to buy requested product
        if current_balance < quantity * price:
            return apology("You can not afford this many units of this product", 400)

        # If all of the above conditions are fulfilled, amount of purchase is substracted from current_balance
        current_balance -= quantity * price

        # Update database
        transaction = "buy"
        accountant.current_balance = current_balance
        transaction = History(transaction=transaction, 
                            product_name=product_name, 
                            quantity=quantity, 
                            price=price, 
                            sale_price=sale_price,
                            value=quantity*price, 
                            accountant_id=accountant_id, user_id=id)
        db.session.add(transaction)
        db.session.commit()

        product = Storage.query.filter_by(accountant_id=accountant_id, product_name=product_name).first()
        if product:
            current_quantity = product.quantity 
            product.quantity = current_quantity + quantity
        else:
            product = Storage(product_name=product_name, 
                            quantity=quantity, 
                            price=price, 
                            sale_price=sale_price, 
                            accountant_id=accountant_id)
            db.session.add(product)
        db.session.commit()
        flash("Purchase successful")
        return redirect("/")
    return render_template("buy.html", current_balance=current_balance)