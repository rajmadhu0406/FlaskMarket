from MARKET import app
from flask import render_template, redirect, url_for, flash, request
from MARKET.model import product, User
from MARKET.form import RegisterForm, LoginForm, SellItemForm, PurchaseItemForm, AddMoney
from MARKET import db
from flask_login import login_user, logout_user, login_required, current_user


# import logging
# from MARKET import templates
# from MARKET.templates import home


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/market", methods=['GET', 'POST'])
@login_required
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 5000},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()
    add_money = AddMoney()
    # if purchase_form.validate_on_submit():
    #     name = request.form.get('purchased_item')
    #     print(name)

    if request.method == "POST":
        #Purchase Logic
        purchased_item = request.form.get('purchased_item')
        product_obj = product.query.filter_by(name=purchased_item).first()
        if product_obj: #check if it is null or not
            if current_user.can_purchase(product_obj):
                product_obj.buy(current_user)
                flash(f"You purchased {product_obj.name} for ${product_obj.price}", category="success")
            else:
                flash("You are short of funds :(", category="danger")

        #Sell Logic

        sold_item = request.form.get('sold_item')
        product_sell_obj = product.query.filter_by(name=sold_item).first()
        if product_sell_obj:
            product_sell_obj.sell(current_user)
            flash(f"You sold {product_sell_obj.name} for ${product_sell_obj.price}", category="success")

        #Add logic

        money_to_add = request.form.get('added_money')
        if money_to_add == None:
            pass
        elif money_to_add != 0:
            current_user.add(money_to_add)
            flash(f"${money_to_add} has been added to your wallet", category="success")
        else:
            flash("Error! There was an error while transfering the money to your account.", category="danger")


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = product.query.filter_by(owner=None)  # SQLAlchemy
        owned_items = product.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, sell_form=sell_form, purchase_form=purchase_form, owned_items=owned_items, add_money=add_money)




@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()

        login_user(user_to_create)
        flash(f'Account created successfully! You are logged in as {user_to_create.username}.', category='success')

        return redirect(url_for('market_page'))
    if form.errors != {}:  # If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'You have logged in successfully as {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password didn\'t match! Please try again.', category='danger')


    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out successfully!', category='info')
    return redirect(url_for("home_page"))
