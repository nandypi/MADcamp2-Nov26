from flask_restful import Api, Resource
from models import db, User, Items
from flask import request

api = Api()

class Hello(Resource):
    def get(self):
        return {"message": "Hello, World!"}
api.add_resource(Hello, '/hello')

class Register(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        name = data.get('name')

        if not email or not name:
            return {"message": "Email and name are required."}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists."}, 400

        new_user = User(email=email, name=name)
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User {name} registered successfully."}, 201
api.add_resource(Register, '/register')

class Item(Resource):
    def get(self, item_id):
        item = Items.query.get(item_id)
        if not item:
            return {"message": "Item not found."}, 404
        return {"id": item.id, "name": item.name, "url": item.url}

    def post(self):
        data = request.get_json()
        name = data.get('name')
        url = data.get('url')

        if not name or not url:
            return {"message": "Name and URL are required."}, 400

        new_item = Items(name=name, url=url)
        db.session.add(new_item)
        db.session.commit()

        return {"message": f"Item {name} created successfully.", "id": new_item.id}, 201
    def put(self, item_id):
        item = Items.query.get(item_id)
        if not item:
            return {"message": "Item not found."}, 404

        data = request.get_json()
        name = data.get('name')
        url = data.get('url')

        if name:
            item.name = name
        if url:
            item.url = url

        db.session.commit()

        return {"message": f"Item {item_id} updated successfully."}
    def delete(self, item_id):
        item = Items.query.get(item_id)
        if not item:
            return {"message": "Item not found."}, 404

        db.session.delete(item)
        db.session.commit()

        return {"message": f"Item {item_id} deleted successfully."}
api.add_resource(Item, '/item', '/item/<int:item_id>')