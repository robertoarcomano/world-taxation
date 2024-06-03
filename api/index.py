from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restx import Api as RestxApi, Resource as RestxResource
from flask_restx.swagger import Swagger

app = Flask(__name__)
api = RestxApi(app)

# Sample data
users = [
    {"id": 1, "name": "John Doe", "email": "john@example.com"},
    {"id": 2, "name": "Jane Smith", "email": "jane@example.com"},
    {"id": 3, "name": "Bob Johnson", "email": "bob@example.com"}
]

# Swagger configuration
SWAGGER_URL = '/api/docs'
API_URL = '/swagger'

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Flask API Example"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/swagger')
def swagger_spec():
    """
    Swagger API specification
    ---
    responses:
      '200':
        description: Successful response
        schema:
          type: object
    """
    swagger = Swagger(api)
    return jsonify(swagger.as_dict())


class UserList(RestxResource):
    """
    Users Resource
    """
    def get(self):
        """
        Get all users
        ---
        responses:
          '200':
            description: Successful response
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                  name:
                    type: string
                  email:
                    type: string
        """
        return jsonify(users)

    def post(self):
        """
        Create a new user
        ---
        parameters:
          - in: body
            name: user
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                email:
                  type: string
        responses:
          '201':
            description: Successful response
            schema:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                email:
                  type: string
        """
        new_user = request.get_json()
        new_user['id'] = len(users) + 1
        users.append(new_user)
        return jsonify(new_user), 201


api.add_resource(UserList, '/users')

if __name__ == '__main__':
    app.run(debug=True)
