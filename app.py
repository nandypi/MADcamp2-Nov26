from flask import Flask, render_template, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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
    app.run(debug=True)