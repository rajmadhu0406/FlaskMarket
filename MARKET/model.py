from MARKET import db
from MARKET import bcrypt
from MARKET import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    # __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    #password = db.Column(db.String(30), nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), nullable = False, default=1000)
    products = db.relationship('product', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}'
        else:
            return f'{self.budget}'

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self,plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):  #checks if entered password and database password is same or not
        return bcrypt.check_password_hash(self.password_hash, attempted_password) #this returns True/False

    def can_purchase(self, p_obj):
        return self.budget >= p_obj.price



class product(db.Model):
    #__tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id')) #user in lowercase
    #changing representation when running query
    def __repr__(self):
        return f'product {self.name}'

    def buy(self, user):
        user.budget -= self.price
        self.owner = user.id
        db.session.commit()

    def sell(self,user):
        user.budget += self.price
        self.owner = None
        db.session.commit()
