from datetime import date
import werkzeug
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
# Imports from local
from tables import db, Product, Sales, Users, sales_products
from forms import CreateSalesForm, CreateProductForm, RegisterForm, LoginForm


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///one-stop-store.db"
db.init_app(app)
# Bootstrap5(app)

# TODO: Configure Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(Users, user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return  abort(403)
        return f(*args, **kwargs)
    return decorated_function


with app.app_context():
    db.create_all()

app.secret_key = "dede557dfjzzd"
bootstrap = Bootstrap5(app)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(Users).where(Users.email == form.email.data)).scalar()
        if user:
            flash('User Already Exists!')
            return redirect(url_for('login'))
        else:
            hashed_password = werkzeug.security.generate_password_hash(password=form.password.data,
                                                                       method='pbkdf2:sha256', salt_length=8)
            new_user = Users(
                email=form.email.data,
                name=form.name.data,
                password=hashed_password
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('home'))
    return render_template('register.html', form=form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(Users).where(Users.email == form.email.data)).scalar()
        user_password = form.password.data
        if user and check_password_hash(user.password, user_password):
            login_user(user)
            return redirect(url_for('home'))
        elif not user:
            flash('You are not registered!')
            return redirect(url_for('register'))
        else:
            flash('Incorrect Password, Please try again.')
            return redirect(url_for('login'))
    return render_template("login.html", form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/products')
def products():
    return render_template('product.html')


@app.route('/add-product', methods= ['GET', 'POST'])
@admin_only
def add_product():
    form = CreateProductForm()
    if form.validate_on_submit():
        product = db.session.execute(db.select(Product).where(Product.name == form.name.data)).scalar()
        if product:
            flash('Product already registered in the database!')
            return redirect(url_for('products'))
        else:
            new_product = Product(
                name=form.name.data,
                price=form.price.data,
                amount_stock=form.amount_stock.data,
                amount_sold=form.amount_sold.data,
                img_url=form.img_url.data,
                barcode=form.barcode.data
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('products'))
    return render_template('add-product.html', form=form, current_user=current_user)

@app.route('/view-product', methods= ['GET', 'POST'])
def view_product():
    all_products = db.session.execute(db.select(Product)).scalars().all()
    return render_template('view-product.html', products=all_products, current_user=current_user)


@app.route("/product/<int:product_id>")
def show_product(product_id):
    requested_product = db.get_or_404(Product, product_id)
    return render_template("show-product.html", product=requested_product, current_user=current_user)


@app.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
@admin_only
def edit_product(product_id):
    requested_product = db.get_or_404(Product, product_id)
    edit_form = CreateProductForm(
        name=requested_product.name,
        price=requested_product.price,
        amount_stock=requested_product.amount_stock,
        amount_sold=requested_product.amount_sold,
        img_url=requested_product.img_url,
        barcode=requested_product.barcode
    )
    if edit_form.validate_on_submit():
        requested_product.name = edit_form.name.data
        requested_product.price = edit_form.price.data
        requested_product.amount_stock = edit_form.amount_stock.data
        requested_product.amount_sold = edit_form.amount_sold.data
        requested_product.img_url = edit_form.img_url.data
        requested_product.barcode = edit_form.barcode.data
        db.session.commit()
        return redirect(url_for("show_product", product_id=product_id))
    return render_template('add-product.html', form=edit_form, current_user=current_user)


@app.route("/delete-product/<int:product_id>")
@admin_only
def delete_product(product_id):
    product_to_delete = db.get_or_404(Product, product_id)
    db.session.delete(product_to_delete)
    db.session.commit()
    return redirect(url_for('view_product'))


if __name__ == "__main__":
    app.run(debug=True)