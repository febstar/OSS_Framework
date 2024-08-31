from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm for creating a product
class CreateProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired()])
    price = StringField("Product Price", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    amount_stock = StringField("Product Amount in Stock", validators=[DataRequired()])
    amount_sold = StringField("Product Amount Sold", validators=[DataRequired()])
    barcode = StringField("Product Barcode", validators=[DataRequired()])
    submit = SubmitField("Submit Product")


# WTForm for creating a sale
class CreateSalesForm(FlaskForm):
    barcode = StringField("Scan Barcode", validators=[DataRequired()])
    quantity = StringField("Enter Amount", validators=[DataRequired()])
    submit = SubmitField("Add to cart")


# WTForm for registering users
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")


# WTForm for logging in users
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")

# TODO: Create a CommentForm so users can leave comments below posts
