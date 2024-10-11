
# 1StopStore

### A Simple Flask-based Storefront Application

1StopStore is a web application built with Flask that simulates an online shopping experience for a one-stop store. This application showcases products, provides a cart management system, and includes functionalities like product search, barcode scanning, and receipt generation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)


---

## Overview

1StopStore is a store management application where users can browse through products, view featured products on the homepage, and manage their shopping cart. It provides a fully dynamic interface for product management and sales recording.

### Store Description

1StopStore is your go-to place for all your needs. From provisions to utilities, clothes, shoes, and much more, we’ve got it all in one place! The application allows customers to easily browse, add items to their cart, and purchase items with the option to print receipts, making it an efficient system for store management.

---

## Features

- **Carousel of Store Images**: A dynamic carousel showcasing images of the store.
- **User Register and Login**: Allows for new users to register and returning users to login
- **Registering New Products**: Adding new products to the store database.
- **Edit Products**: Changing info on akready existing products in the database. 
- **Product Showcase**: Displays a selection of random products from the database with their image and price.
- **Add to Cart**: Dynamically add products to the cart with customizable quantities.
- **Clear Cart**: Functionality to clear the cart with a single click.
- **Product Search**: Allows users to search for products by name or scan a barcode.
- **Receipt Generation**: Print a receipt for each sale.
- **Responsive Design**: The interface is mobile-friendly and responsive.

---

## Technologies

- **Python**: Backend logic and routing.
- **Flask**: Web framework.
- **SQLAlchemy**: ORM for database management.
- **HTML/CSS/JavaScript**: Frontend design and functionality.
- **Jinja2**: Templating engine for dynamic HTML generation.
- **SQLite**: Database used for storing products, sales, and user data.
- **Bootstrap**: CSS framework for responsive design.

---

## Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/febstar/cafe-RESTFUL-api-flask.git
   ```

2. Navigate to the project directory:

   ```bash
   cd 1StopStore
   ```

3. Set up and activate a Python virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

6. Run the application:

   ```bash
   flask run
   ```

7. Open your browser and visit:

   ```
   http://127.0.0.1:5000
   ```

---

## Usage

### Homepage

- View store description and images.
- Browse featured products.

### Product Management

- Add products to the cart.
- Adjust product quantities.
- Search products by name or barcode.
- Clear the cart with the "Clear Cart" button.
- Print a receipt for completed purchases.

### Admin Access

- Admin users can manage product inventories.
- Generate daily reports on sales.

---

## Screenshots

- **Home Page**: Displays the store's description, images, and some featured products.
- **Product Cart**: Dynamically add and remove products to/from the shopping cart.
- **Receipt Printing**: Automatically generate receipts upon payment.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Open a Pull Request.

---

### Credits
Created by [Onyeyili Febechukwu Owen](https://github.com/febstar).
