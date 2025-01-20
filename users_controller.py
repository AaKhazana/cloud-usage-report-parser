from flask import Blueprint, jsonify, request, session
from utils import validate_user_data, authenticated
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite
from enum import Enum

users_controller = Blueprint('user_controller', __name__)

# TODO: Add user roles validation

# TODO: Implement the following routes
# DELETE /users/delete/<id> - Delete user by id


class UserColumns(Enum):
    ID = 0
    FULL_NAME = 1
    EMAIL = 2
    ORGANIZATION = 3
    ADDRESS = 4
    NTN_NUMBER = 5
    PASSWORD_HASH = 6
    IS_ACTIVE = 7
    IS_ADMIN = 8
    CREATED_AT = 9
    UPDATED_AT = 10


@users_controller.route('/get', methods=['GET'])
def get_all_users():
    if not authenticated():
        return jsonify({"message": "Not authorized!"}), 401

    is_admin = session['user'][UserColumns.IS_ADMIN.value]
    if not is_admin:
        return jsonify({"message": "Not authorized!"}), 401

    db = sqlite.DatabaseService()
    query = "SELECT * FROM users"
    result = db.run_query(query)
    if not result:
        return jsonify({"message": "No Users found"}), 404

    response = []
    for user in result:
        flags = {
            "Active": user[UserColumns.IS_ACTIVE.value],
            "Admin": user[UserColumns.IS_ADMIN.value]
        }
        user_data = {
            'id': user[UserColumns.ID.value],
            'full_name': user[UserColumns.FULL_NAME.value],
            'email': user[UserColumns.EMAIL.value],
            'organization': user[UserColumns.ORGANIZATION.value],
            # 'address': user[UserColumns.ADDRESS.value],
            # 'ntn_number': user[UserColumns.NTN_NUMBER.value],
            'flags': flags,
            'created_at': user[UserColumns.CREATED_AT.value],
            'updated_at': user[UserColumns.UPDATED_AT.value]
        }
        response.append(user_data)
    return jsonify({"message": "List of Users", "data": response})


@users_controller.route('/get/<id>', methods=['GET'])
def get_user(id):
    user_id = int(id)

    if not authenticated():
        return jsonify({"message": "Not authorized!"}), 401

    is_admin = session['user'][UserColumns.IS_ADMIN.value]
    if not is_admin:
        if user_id != session['user'][UserColumns.ID.value]:
            return jsonify({"message": "Not authorized!"}), 401

    db = sqlite.DatabaseService()
    query = "SELECT * FROM users WHERE id = ?"
    result = db.run_query(query, (user_id,))
    if not result:
        return jsonify({"message": "User not found"}), 404

    user = result[0]
    flags = {
        "Active": user[UserColumns.IS_ACTIVE.value],
        "Admin": user[UserColumns.IS_ADMIN.value]
    }
    user_info = {
        'id': user[UserColumns.ID.value],
        'full_name': user[UserColumns.FULL_NAME.value],
        'email': user[UserColumns.EMAIL.value],
        'organization': user[UserColumns.ORGANIZATION.value],
        'address': user[UserColumns.ADDRESS.value],
        'ntn_number': user[UserColumns.NTN_NUMBER.value],
        'flags': flags,
        'created_at': user[UserColumns.CREATED_AT.value],
        'updated_at': user[UserColumns.UPDATED_AT.value]
    }

    return jsonify({"message": "User Data", "data": user_info})


@users_controller.route('/create', methods=['POST'])
def create_user():
    """
    Create New User
    """
    data = request.get_json()

    # if not authenticated():
    #     return jsonify({"message": "Not authorized!"}), 401

    # is_admin = session['user'][UserColumns.IS_ADMIN.value]
    # if not is_admin:
    #     return jsonify({"message": "Not authorized!"}), 401

    # if not data:
    #     return jsonify({"message": "No data provided"}), 400

    validation_result, validation_error = validate_user_data(data)
    if not validation_result:
        return jsonify({"message": validation_error}), 400

    db = sqlite.DatabaseService()

    check_user_query = "SELECT * FROM users WHERE email = ?"
    user = db.run_query(check_user_query, (data["email"],))

    if user:
        return jsonify({"message": "User with email already exists"}), 400

    password_hash = generate_password_hash(data["password"])

    insert_user_query = """INSERT INTO users (full_name, email, organization, address, ntn_number, password_hash, is_active, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""

    user_id = db.run_query(
        insert_user_query,
        (
            data["full_name"],
            data["email"],
            data.get("organization", None),
            data.get("address", None),
            data.get("ntn_number", None),
            password_hash,
            data.get("is_active", False),
            data.get("is_admin", False),
        )
    )

    db.commit()

    return jsonify({"message": "User added successfully", "user_id": user_id})


@users_controller.route('/update', methods=['POST'])
def update_user():
    data = request.get_json()

    if not authenticated():
        return jsonify({"message": "Not authorized!"}), 401

    is_admin = session['user'][UserColumns.IS_ADMIN.value]
    if not is_admin:
        return jsonify({"message": "Not authorized!"}), 401

    if not data:
        return jsonify({"message": "No data provided"}), 400

    if not data.get('user_id'):
        return jsonify({"message": "No user id provided"}), 400

    db = sqlite.DatabaseService()

    user_id = data['user_id']

    check_user_query = "SELECT * FROM users WHERE id = ?"
    result = db.run_query(check_user_query, (user_id,))
    if not result:
        return jsonify({"message": "Invalid user provided"}), 400

    user = result[0]

    update_user_query = "UPDATE users SET full_name = ?, email = ?, organization = ?, address = ?, ntn_number = ?, is_active = ?, is_admin = ? WHERE id = ?"
    result = db.run_query(
        update_user_query,
        (
            data.get("full_name", user[UserColumns.FULL_NAME.value]),
            data.get("email", user[UserColumns.EMAIL.value]),
            data.get("organization", user[UserColumns.ORGANIZATION.value]),
            data.get("address", user[UserColumns.ADDRESS.value]),
            data.get("ntn_number", user[UserColumns.NTN_NUMBER.value]),
            data.get("is_active", user[UserColumns.IS_ACTIVE.value]),
            data.get("is_admin", user[UserColumns.IS_ADMIN.value]),
            user_id,
        )
    )

    db.commit()

    return jsonify({"message": "user updated successfully!"})


@users_controller.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    if not data:
        return jsonify({"message": "Invalid credentials"}), 401

    if not data.get('email'):
        return jsonify({"message": "Invalid credentials"}), 401

    if not data.get('password'):
        return jsonify({"message": "Invalid credentials"}), 401

    db = sqlite.DatabaseService()
    check_user_query = "SELECT * FROM users WHERE email = ?"
    result = db.run_query(check_user_query, (data['email'],))
    if not result:
        return jsonify({"message": "Invalid credentials"}), 401

    user = result[0]
    if not check_password_hash(user[UserColumns.PASSWORD_HASH.value], data['password']):
        return jsonify({"message": "Invallid credentials"}), 401

    session['user'] = user

    flags = {
        "Active": user[UserColumns.IS_ACTIVE.value],
        "Admin": user[UserColumns.IS_ADMIN.value]
    }

    user_info = {
        'id': user[UserColumns.ID.value],
        'full_name': user[UserColumns.FULL_NAME.value],
        'email': user[UserColumns.EMAIL.value],
        'organization': user[UserColumns.ORGANIZATION.value],
        'address': user[UserColumns.ADDRESS.value],
        'flags': flags,
        'ntn_number': user[UserColumns.NTN_NUMBER.value],
        'created_at': user[UserColumns.CREATED_AT.value],
        'updated_at': user[UserColumns.UPDATED_AT.value]
    }

    return jsonify({"message": "Logged in successfully!", "data": user_info})


@users_controller.route('/logout', methods=['get'])
def logout_user():
    session.pop('user', None)
    return jsonify({"message": "Logged out successfully!"})
