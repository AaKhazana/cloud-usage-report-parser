from flask import Blueprint, jsonify, request
from utils import validate_user_data
from werkzeug.security import generate_password_hash
import sqlite

users_controller = Blueprint('user_controller', __name__)

# TODO: Add Session Management and user roles validation

# TODO: Implement the following routes
# 1. GET /users/get/<id> - Get single user by id
# 2. POST /users/update - Update user by id
# 3. DELETE /users/delete/<id> - Delete user by id


@users_controller.route('/get', methods=['GET'])
def get_all_users():
    db = sqlite.DatabaseService()
    query = "SELECT * FROM users"
    result = db.run_query(query)
    if not result:
        return jsonify({"error": "No Users found"}), 404

    response = []
    for user in result:
        flags = {
            "Active": user[5],
            "Admin": user[6]
        }
        user_data = {
            'id': user[0],
            'full_name': user[1],
            'email': user[2],
            'organization': user[3],
            'flags': flags,
            'created_at': user[7],
            'updated_at': user[8]
        }
        response.append(user_data)
    return jsonify({"message": "List of Users", "data": response})


@users_controller.route('/create', methods=['POST'])
def create_user():
    """
    Create New User
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    validation_result, validation_error = validate_user_data(data)
    if not validation_result:
        return jsonify({"error": validation_error}), 400

    db = sqlite.DatabaseService()

    check_user_query = "SELECT * FROM users WHERE email = ?"
    user = db.run_query(check_user_query, (data["email"],))

    if user:
        return jsonify({"error": "User with email already exists"}), 400

    password_hash = generate_password_hash(data["password"])

    insert_user_query = """INSERT INTO users (full_name, email, organization, password_hash, is_active, is_admin) VALUES (?, ?, ?, ?, ?, ?)"""

    user_id = db.run_query(
        insert_user_query,
        (
            data["full_name"],
            data["email"],
            data.get("organization", None),
            password_hash,
            data.get("is_active", False),
            data.get("is_admin", False)
        )
    )

    db.commit()

    return jsonify({"message": "User added successfully", "user_id": user_id})
