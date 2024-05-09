# Description: This file contains the main code for the web application.
from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy

import random
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

db = SQLAlchemy(app)

class Cart_Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_image = db.Column(db.String(80), nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.username

class Product_info(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)
    product_price = db.Column(db.Integer, nullable=False)
    product_description = db.Column(db.String(120), nullable=False)
    product_image = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    orders = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Inventory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coffee_bags = db.Column(db.Integer, nullable=False)
    sugar_packets = db.Column(db.Integer, nullable=False)
    creamer_packets = db.Column(db.Integer, nullable=False)
    cups = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<User %r>' % self.username

# Set up the application context and perform database operations
# with app.app_context():
#     db.create_all()


@app.route('/add_to_cart', methods=['POST', 'GET'])
def add_to_cart():
    id = request.form['product_id']
    name = request.form['product_name']
    price = request.form['product_price']
    image = request.form['product_image']
    quantity = request.form['product_quantity']
    print(id, name, price)
    new_product = Cart_Product(id=id, product_name=name, product_price=price, product_image=image,
                               product_quantity=quantity)
    try:
        db.session.add(new_product)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()

    return redirect(request.referrer)

@app.route('/update_quantity', methods=['POST', 'GET'])
def update_quantity():
    id = request.form['id']
    quantity = request.form['quantity']
    print(id, quantity)
    product = Cart_Product.query.get_or_404(id, description='There is no product with that ID')
    product.product_quantity = quantity
    db.session.commit()

    return redirect(request.referrer)


@app.route('/remove_from_cart', methods=['POST', 'GET'])
def remove_from_cart():
    id = request.form['id']
    Cart_Product.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(request.referrer)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/product/coffee')
def coffee_all():  # put application's code here
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'product_info'")
    rows = cursor.fetchall()

    # for row in rows:
    #     print(row[1])
    # Close the database connection
    conn.close()
    return render_template('shop-full-width.html', rows=rows)


@app.route('/product/cart')
def cart():
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'cart__product'")
    rows = cursor.fetchall()

    # for row in rows:
    #     print(row[1])
    # Close the database connection

    conn.close()
    return render_template('cart.html', rows=rows)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact')
def contact():
    return render_template('contact-us.html')



@app.route('/checkout')
def checkout():
    total_items_in_order = ""
    #total price counter
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'cart__product'")
    rows = cursor.fetchall()

    totat_price = 0
    for row in rows:
        totat_price += row[2]*row[4]
        order_product = "[ " + row[1] + " | Q-" + str(row[4]) + " | $-" + str(row[2]) + " ], "
        total_items_in_order += order_product
    conn.close()
    print(total_items_in_order)

    new_order = Orders(orders=total_items_in_order)
    try:
        db.session.add(new_order)
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    db.session.query(Cart_Product).delete()
    db.session.commit()

    return render_template('checkout.html', totat_price=totat_price)


@app.route('/policy')
def policy():
    return render_template('policy.html')


# ____________________________________________________________

@app.route('/orders')
def orders():
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'orders'")
    rows = cursor.fetchall()

    for row in rows:
        print(row[1])
    # Close the database connection
    conn.close()
    return render_template('orders.html', rows=rows)

@app.route('/orders/delete', methods=['POST', 'GET'])
def delete_orders():
    id = request.form['id']
    Orders.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect(request.referrer)

@app.route('/orders/fulfilled', methods=['POST', 'GET'])
def fulfilled_orders():
    id = request.form['id']
    Orders.query.filter_by(id=id).delete()
    db.session.commit()

    inventory = Inventory.query.first()
    inventory.coffee_bags -= random.randint(1, 4)
    inventory.sugar_packets -= random.randint(1, 10)
    inventory.creamer_packets -= random.randint(1, 7)
    inventory.cups -=  random.randint(1, 3)

    db.session.commit()

    return redirect(request.referrer)

@app.route('/inventory')
def inventory():
    conn = sqlite3.connect('instance/items.db')
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT * FROM 'inventory'")
    rows = cursor.fetchall()

    # for row in rows:
    #     print(row[1])
    # Close the database connection
    conn.close()
    return render_template('inventory.html', rows=rows)

@app.route('/inventory/update', methods=['POST', 'GET'])
def update_inventory():
    coffee_bags = request.form['coffee_bags']
    sugar_packets = request.form['sugar_packets']
    creamer_packets = request.form['creamer_packets']
    cups = request.form['cups']

    inventory = Inventory.query.first()
    inventory.coffee_bags = coffee_bags
    inventory.sugar_packets = sugar_packets
    inventory.creamer_packets = creamer_packets
    inventory.cups = cups

    db.session.commit()

    return redirect(request.referrer)








if __name__ == '__main__':
    app.run(debug=True)
