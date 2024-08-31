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
sales_products = Table(
    'sales_products', Base.metadata,
    Column('product_id', Integer, ForeignKey('product.id'), primary_key=True),
    Column('sale_id', Integer, ForeignKey('sales.id'), primary_key=True),
    Column('quantity', Integer, nullable=False, default=1)  # Quantity sold in the sale
)


class Product(db.Model):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True)
    price: Mapped[int] = mapped_column(Integer)
    amount_stock: Mapped[int] = mapped_column(Integer)
    amount_sold: Mapped[int] = mapped_column(Integer)
    img_url: Mapped[str] = mapped_column(String(250))
    barcode: Mapped[int] = mapped_column(Integer)

    # Many-to-many relationship with Sales
    sales = relationship('Sales', secondary=sales_products, back_populates='products')


class Sales(db.Model):
    __tablename__ = "sales"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[str] = mapped_column(String(100))
    closing_balance: Mapped[int] = mapped_column(Integer)

    # Many-to-many relationship with Products
    products = relationship('Product', secondary=sales_products, back_populates='sales')


class Users(UserMixin, db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(250), unique=True)
    password: Mapped[str] = mapped_column(String(250))