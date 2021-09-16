from MARKET import app
from flask import render_template
from MARKET.models import Item
from MARKET.forms import RegisterForm


@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')

@app.route("/market")
def market_page():
    # items = [
    #     {'id': 1, 'name': 'Phone', 'barcode': '893212299897', 'price': 5000},
    #     {'id': 2, 'name': 'Laptop', 'barcode': '123985473165', 'price': 900},
    #     {'id': 3, 'name': 'Keyboard', 'barcode': '231985128446', 'price': 150}
    # ]
    items = product.query.all() #SQLAlchemy
    return render_template('market.html', items=items)

@app.route('/register')
def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)