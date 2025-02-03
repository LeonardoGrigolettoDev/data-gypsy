from flask import request, jsonify, Blueprint
from app.models import Model
import app.services.users as service_users
import psycopg2.errors as pg_errors
general_routes = Blueprint('general_routes', __name__)

@general_routes.route('/data/load/<permission>', methods=['POST'])
def upload_file(permission):
    file = request.files.get('file')
    if permission not in ['public', 'private']:
        return {"message":'Param "permission" was not informed'}, 400
    print(file.filename)
    typeFile = file.filename.split('.')[-1]
    match typeFile:
        case 'csv':
            return {"message":'Data loaded successfully'}, 200
            
        case _:
            return {"message":'Not implemented'}, 501

@general_routes.route('/login', methods=['POST'])
def auth():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return {"message": "Missing params"}, 400
    try:
        found = service_users.auth_user(email, password)
    except Exception as e:
        return {"message": f"Unable to authenticate user: {e}"}, 400
    else:
        if not found:
            return {"message": "Incorrect authentication"}, 401
        return {"message": {"id": found}}, 200


@general_routes.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
    permission = data.get('permission')
    email = data.get('email')
    password = data.get('password')
    if not name or not permission or not email or not password:
        return {"message": "Could not find all params to create"}, 400
    try:
        created = service_users.create_user({
            "name": name,
            "permission": permission,
            "email": email,
            "password": password
        })
    except Exception as e:
        return {"message": f"Could not create user: {e}"}, 400
    else:
        if isinstance(created, pg_errors.UniqueViolation):
            return {"message": f"User already exists on DB"}, 200
        return {"message": f"User created successfully"}, 201

