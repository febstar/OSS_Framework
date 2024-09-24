import random
from datetime import date
import werkzeug
from flask import Flask, abort, render_template, redirect, url_for, flash, jsonify, request
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
from tables import db, Product, Sale, Users, SalesItem, ClosingBalance
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
    all_products = db.session.execute(db.select(Product)).scalars().all()
    return render_template('index.html', products=all_products)


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


@app.route("/sales")
@admin_only
def sales():
    return render_template('sales.html')


@app.route('/record-sale')
@admin_only
def record_sale_page():
    return render_template('record-sales.html')


# Search product by barcode or name (dynamic search)
@app.route('/search_product')
def search_product():
    query = request.args.get('q', '')
    products = Product.query.filter(
        (Product.name.ilike(f'%{query}%')) |
        (Product.barcode == query)
    ).all()
    return jsonify({
        'products': [{'id': p.id, 'name': p.name, 'price': p.price} for p in products]
    })


# Record sale
@app.route('/record_sale', methods=['POST'])
def record_sale():
    data = request.json
    cart = data['cart']

    # Create a new sale
    new_sale = Sale(total_amount=0)
    db.session.add(new_sale)
    db.session.flush()  # Get the sale ID before committing

    total_sale_value = 0

    # Add products from the cart
    for item in cart:
        product = Product.query.get(item['id'])
        quantity = int(item['quantity'])

        # Update stock and amount sold
        if product.amount_stock < quantity:
            return jsonify({'error': f'Not enough stock for {product.name}'}), 400

        product.amount_stock -= quantity
        product.amount_sold += quantity

        # Create SalesItem for each product
        sale_item = SalesItem(
            sale_id=new_sale.id,
            product_id=product.id,
            quantity=quantity,
            unit_price=product.price
        )
        db.session.add(sale_item)

        total_sale_value += quantity * product.price

    new_sale.total_amount = total_sale_value
    db.session.commit()

    return jsonify({'sale_id': new_sale.id}), 201



# Generate and print receipt
@app.route('/print_receipt/<int:sale_id>')
def print_receipt(sale_id):
    sale = Sale.query.get(sale_id)
    if not sale:
        return "Sale not found", 404

    # Get all items in this sale
    sale_items = SalesItem.query.filter_by(sale_id=sale_id).all()

    # Prepare data for rendering
    products = []
    total = 0
    for item in sale_items:
        product = Product.query.get(item.product_id)
        subtotal = item.quantity * item.unit_price
        products.append({
            'name': product.name,
            'quantity': item.quantity,
            'unit_price': item.unit_price,
            'subtotal': subtotal
        })
        total += subtotal

    # Render the receipt page
    return render_template('receipt.html', sale=sale, products=products, total=total)


@app.route('/view-sales', methods=["POST", "GET"])
@admin_only
def view_sales():
    all_sales = db.session.execute(db.select(Sale)).scalars().all()
    return render_template('view-sales.html', sales=all_sales, current_user=current_user)


# @app.route("/delete-sale/<int:sale_id>")
# @admin_only
# def delete_sale(sale_id):
#     sale_to_delete = db.get_or_404(Sale, sale_id)
#     db.session.delete(sale_to_delete)
#     db.session.commit()
#     return redirect(url_for('view_sales'))


if __name__ == "__main__":
    app.run(debug=False)