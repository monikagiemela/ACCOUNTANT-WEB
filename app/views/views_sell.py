from flask import flash, redirect, render_template, request, session

from app import app, db
from app.models import Accountants, Storage, History
from app.UTILS.helpers import apology, login_required


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    id = session.get("user_id")
    accountant_id = session.get("accountant_id")
    accountant = Accountants.query.filter_by(id=accountant_id).first()    
    current_balance = accountant.current_balance
    products = Storage.query.filter_by(accountant_id=accountant_id).all()
    if request.method == "GET":
        list_of_products = []
        for product in products:
            if product.quantity > 0 and product.product_name not in list_of_products:              
                list_of_products.append(product.product_name)
        context = {
            "current_balance": current_balance,
            "list_of_products": list_of_products
        }
        return render_template("sell.html", context=context)

    else:
        # Checkes if user chose a product_name
        product_name = request.form.get("product_name").lower()
        if not product_name:
            return apology("Choose a product", 403)
  
        # Checks if user entered a valid number of product
        try:
            quantity = float(request.form.get("quantity"))
        except:
            return apology("Quantity must be a positive integer", 400)
        if quantity <= 0:
            return apology("Quantity must be a positive integer", 400)
        
        try:
            price = float(request.form.get("price"))
        except:
            return apology("Price must be a positive value", 400)
        if price <= 0:
            return apology("Price must be a positive value", 400)

        # Check if accountant owns enough product
        product = Storage.query.filter_by(accountant_id=accountant_id, product_name=product_name).first()
        if not product:    
            return apology("This product is not available", 400)
        
        product_quantity = product.quantity
        if product_quantity < quantity:
            return apology(f"{product_name} availability: { product_quantity } units", 400)

        # Updated database
        transaction = "sell"
        accountant.current_balance += (price * quantity)
        transaction = History(transaction=transaction, product_name=product_name, 
                        quantity=quantity, price=price, value=quantity*price,
                        accountat_id=accountant_id, user_id=id)
        db.session.add(transaction)
        product.quantity -= quantity
        accountant.current_balance += quantity * price
        db.session.commit()

        flash(f"You have successfully sold {quantity} units of {product_name}")
        return redirect("/")