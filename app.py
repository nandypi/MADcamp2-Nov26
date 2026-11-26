from flask import Flask, render_template, request
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this to a random secret key
jwt = JWTManager(app)

# initialize the apis
from apis import api, Resource, cache
api.init_app(app)
app.config['CACHE_TYPE'] = 'RedisCache'  # Use simple in-memory cache
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'  # Redis server URL
cache.init_app(app)

# configure the database
from models import db, User
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)

message_data = "Welcome to the Mad1 bootcamp!"

@app.route('/mad1')
def mad1():
    message = message_data
    return render_template('mad1.html', message=message)

# @app.route('/mad2', methods=['GET', 'POST'])
# def mad2():
#     if request.method == 'GET':
#         message = message_data.replace("Mad1", "Mad2")
#         return {"message": message}
#     elif request.method == 'POST':
#         return {"message": "POST method is not allowed for this route."}, 405

class Mad2(Resource):
    def get(self):
        message = message_data.replace("Mad1", "Mad2")
        return {"message": message}
    def post(self):
        return {"message": "POST method is not allowed for this route."}, 405
api.add_resource(Mad2, '/mad2')

if __name__ == "__main__":
    with app.app_context():
        admin_user = db.session.query(db.exists().where(User.role == 'admin')).scalar()
        if not admin_user:
            admin = User(email='admin@gmail.com', name='Admin', password='password', role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created with email: admin@gmail.com and password: password")
        else:
            print("Admin user already exists with email: admin@gmail.com and password: password")
        db.create_all()
    app.run(debug=True)