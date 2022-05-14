from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from data import users, offers, orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


# def order_new():
#     orders_list = []
#     for order in orders:
#         orders_list.append(order)
#     print(orders_list)
#
# order_new()
class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    executor_id = db.Column(db.Integer)


def orders():
    order_new = []
    for order in orders:
        order_new.append(
            Order(
                id=order['id'],
                name=order['name'],
                description=order['description'],
                start_date=order['start_date'],
                end_date=order['end_date'],
                address=order['address'],
                price=order['price'],
                customer_id=order['customer_id'],
                executor_id=order['executor_id'],
            )
        )
    with db.session.begin():
        db.session.add_all(order_new)

db.create_all()
print(Order.query.get(1).name)
