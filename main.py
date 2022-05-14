import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify
from data import users, offers, orders

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(100))
    phone = db.Column(db.String(100))


class Order(db.Model):
    __tablename__ = 'order'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(100))
    start_date = db.Column(db.String)
    end_date = db.Column(db.String)
    address = db.Column(db.String(100))
    price = db.Column(db.Integer)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    __tablename__ = 'offer'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


def main():
    db.create_all()
    request_data()
    app.run(debug=True)


def request_data():
    users_new = []
    for user in users:
        users_new.append(
            User(
                id=user['id'],
                first_name=user['first_name'],
                last_name=user['last_name'],
                age=user['age'],
                email=user['email'],
                role=user['role'],
                phone=user['phone'],
            )
        )
        with db.session.begin():
            db.session.add_all(users_new)

    offers_new = []
    for offer in offers:
        offers_new.append(
            Offer(
                id=offer['id'],
                order_id=offer['order_id'],
                executor_id=offer['executor_id']
            )
        )
        with db.session.begin():
            db.session.add_all(offers_new)

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


@app.route('/offers', methods=['GET', 'POST'])
def offers_in():
    data = []
    if request.method == 'GET':
        for offer in Offer.query.all():
            data.append({
                "id": offer.id,
                "order_id": offer.order_id,
                "executor_id": offer.executor_id
            })
    elif request.method == 'POST':
        data = request.get_json()
        offer_new = Offer(
            id=data['id'],
            order_id=data['order_id'],
            executor_id=data['executor_id']
        )
        with db.session.begin():
            db.session.add(offer_new)

    return jsonify(data)


@app.route('/users', methods=['GET', 'POST'])
def users_in():
    data = []
    if request.method == 'GET':
        for user in User.query.all():
            data.append({
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "age": user.age,
                "email": user.email,
                "role": user.role,
                "phone": user.phone
            })
    elif request.method == 'POST':
        data = request.get_json()
        user_new = Order(
            id=data['id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            age=data['age'],
            email=data['email'],
            role=data['role'],
            phone=data['phone'],
        )
        with db.session.begin():
            db.session.add(user_new)
    return jsonify(data)


@app.route('/orders', methods=['GET', 'POST'])
def orders_in():
    data = []
    if request.method == 'GET':
        for order in Order.query.all():
            data.append({
                "id": order.id,
                "name": order.name,
                "description": order.description,
                "start_date": order.start_date,
                "end_date": order.end_date,
                "address": order.address,
                "price": order.price,
                "customer_id": order.customer_id,
                "executor_id": order.executor_id,
            })
    elif request.method == 'POST':
        data = request.get_json()
        order_new = Offer(
            Order(
                id=data['id'],
                name=data['name'],
                description=data['description'],
                start_date=data['start_date'],
                end_date=data['end_date'],
                address=data['address'],
                price=data['price'],
                customer_id=data['customer_id'],
                executor_id=data['executor_id']
            )
        )
        with db.session.begin():
            db.session.add_all(order_new)
    return jsonify(data)


@app.route('/offers/<int:oid>', methods=['GET', 'PUT'])
def offers_action(oid):
    if request.method == 'GET':
        offer = Offer.query.get(oid)
        data = {
            "id": offer.id,
            "order_id": offer.order_id,
            "executor_id": offer.executor_id
        }
        return jsonify(data)
    elif request.method == 'PUT':
        data = request.get_json()
        offer = Offer.query.get(oid)
        offer.id = data['id']
        offer.order_id = data['order_id']
        offer.executor_id = data['executor_id']

        with db.session.begin():
            db.session.add_all(offer)


@app.route('/users/<int:uid>', methods=['GET', 'PUT'])
def users_action(uid):
    if request.method == 'GET':
        user = User.query.get(uid)
        data = {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "age": user.age,
            "email": user.email,
            "role": user.role,
            "phone": user.phone
        }
        return jsonify(data)
    elif request.method == 'PUT':
        data = request.get_json()
        user = User.query.get(uid)
        user.id = data['id']
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        with db.session.begin():
            db.session.add_all(user)


@app.route('/orders/<int:oid>', methods=['GET', 'PUT'])
def order_action(oid):
    if request.method == 'GET':
        order = Order.query.get(oid)
        data = {
            "id": order.id,
            "name": order.name,
            "description": order.description,
            "start_date": order.start_date,
            "end_date": order.end_date,
            "address": order.address,
            "price": order.price,
            "customer_id": order.customer_id,
            "executor_id": order.executor_id,
        }
        return jsonify(data)
    elif request.method == 'PUT':
        data = request.get_json()
        order = Order.query.get(oid)
        order.id = data['id'],
        order.name = data['name'],
        order.description = data['description'],
        order.start_date = data['start_date'],
        order.end_date = data['end_date'],
        order.address = data['address'],
        order.price = data['price'],
        order.customer_id = data['customer_id'],
        order.executor_id = data['executor_id']

        with db.session.begin():
            db.session.add_all(order)


@app.route('/delete/<lists>/<oid>', methods=['DELETE'])
def delete_list(lists, oid):
    if lists == offers:
        offer = Offer.query.get(oid)
        db.session.delete(offer)
        db.session.commit()
    elif lists == orders:
        order = Order.query.get(oid)
        db.session.delete(order)
        db.session.commit()
    elif lists == users:
        user = User.query.get(oid)
        db.session.delete(user)
        db.session.commit()


if __name__ == '__main__':
    main()
