import json

from flask import Flask, render_template, url_for, request, jsonify, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///items.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Set up the application context and perform database operations
# with app.app_context():
#     db.create_all()
@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')

@app.route('/product/coffee')
def coffee_all():  # put application's code here
    return render_template('shop-full-width.html')

@app.route('/product/cart')
def cart():
    return render_template('cart.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact-us')
def contact():
    return render_template('contact-us.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/d-cart')
def d_cart():
    return render_template('d-cart.html')

if __name__ == '__main__':
    app.run(debug=True)
