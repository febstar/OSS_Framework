from datetime import date

import werkzeug
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text, ForeignKey, Table, Column
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# Association table for many-to-many relationship between Sales and Products
# sales_products = Table(
#     'sales_products', Base.metadata,
#     Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
#     Column('sale_id', Integer, ForeignKey('sales.id'), primary_key=True),
#     Column('quantity', Integer, nullable=False, default=1)  # Quantity sold in the sale
# )


class Product(db.Model):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    price: Mapped[int] = mapped_column(Integer)
    amount_stock: Mapped[int] = mapped_column(Integer)
    amount_sold: Mapped[int] = mapped_column(Integer)
    img_url: Mapped[str] = mapped_column(String(250))
    barcode: Mapped[int] = mapped_column(Integer)

    # Relationship to SalesItems
    sales_items = relationship("SalesItem", back_populates="product")


# Define Sale Model
class Sale(db.Model):
    __tablename__ = "sales"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=db.func.current_timestamp())
    total_amount = db.Column(db.Integer, nullable=False)

    # Relationship to SalesItems
    items = relationship("SalesItem", back_populates="sale")


# Define SalesItem Model for many-to-many relationship
class SalesItem(db.Model):
    __tablename__ = "sales_items"
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey('sales.id'), nullable=False)  # References 'sales'
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)  # References 'product'
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)

    # Relationships
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product", back_populates="sales_items")

    # Auto-calculate subtotal for this item
    @property
    def subtotal(self):
        return self.quantity * self.unit_price


# Define ClosingBalance Model
class ClosingBalance(db.Model):
    __tablename__ = "closing_balance"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    total_sales = db.Column(db.Integer, nullable=False)
    closing_balance = db.Column(db.Integer, nullable=False)


# Define Users Model
class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250))  # Changed to str, not int
    email: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(250))