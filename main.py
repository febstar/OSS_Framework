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



if __name__ == "__main__":
    app.run(debug=True)