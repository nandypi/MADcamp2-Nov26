from flask_restful import Api, Resource
from models import db, User, Items
from flask import request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

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
        password = data.get('password')

        if not email or not name or not password:
            return {"message": "Email, name, and password are required."}, 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {"message": "User already exists."}, 400

        new_user = User(email=email, name=name, password=password)
        db.session.add(new_user)
        db.session.commit()

        return {"message": f"User {name} registered successfully."}, 201
api.add_resource(Register, '/register')

class Login(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"message": "Email and password are required."}, 400

        user = User.query.filter_by(email=email, password=password).first()
        if not user:
            return {"message": "Invalid credentials."}, 401

        access_token = create_access_token(identity=user.email)
        return {"message": "Login successful.", "access_token": access_token, "role": user.role}, 200
api.add_resource(Login, '/login')

def is_admin():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    return user and user.role == 'admin'

class Item(Resource):
    @jwt_required()
    def get(self, item_id=None):
        if item_id is None:
            items = Items.query.all()
            return [{"id": item.id, "name": item.name, "url": item.url} for item in items]
        item = Items.query.get(item_id)
        if not item:
            return {"message": "Item not found."}, 404
        return {"id": item.id, "name": item.name, "url": item.url}

    @jwt_required()
    def post(self):
        if not is_admin():
            return {"message": "Admin privileges required."}, 403
        data = request.get_json()
        name = data.get('name')
        url = data.get('url')

        if not name or not url:
            return {"message": "Name and URL are required."}, 400

        new_item = Items(name=name, url=url)
        db.session.add(new_item)
        db.session.commit()

        return {"message": f"Item {name} created successfully.", "id": new_item.id}, 201
    
    @jwt_required()
    def put(self, item_id):
        if not is_admin():
            return {"message": "Admin privileges required."}, 403
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
    
    @jwt_required()
    def delete(self, item_id):
        if not is_admin():
            return {"message": "Admin privileges required."}, 403
        item = Items.query.get(item_id)
        if not item:
            return {"message": "Item not found."}, 404

        db.session.delete(item)
        db.session.commit()

        return {"message": f"Item {item_id} deleted successfully."}
api.add_resource(Item, '/items', '/items/<int:item_id>')