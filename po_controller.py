from flask import Blueprint, jsonify, request, session
from po_service import get_po, add_po, update_po
from users_controller import UserColumns
from utils import authenticated
import sqlite

po_controller = Blueprint("po_controller", __name__)


@po_controller.route('/create', methods=['POST'])
def create_purchase_order():
    if not authenticated():
        return jsonify({"message": "Not authorized!"}), 401

    is_admin = session['user'][UserColumns.IS_ADMIN.value]
    if not is_admin:
        return jsonify({"message": "Not authorized!"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"}), 400

    if not data.get('userId'):
        return jsonify({"message": "No user id provided"}), 400

    if not data['services']:
        return jsonify({"message": "Missing services"}), 400

    db = sqlite.DatabaseService()

    user_id = data['userId']

    check_user_query = "SELECT * FROM users WHERE id = ?"

    query_response = db.run_query(check_user_query, (user_id,))
    if not query_response:
        return jsonify({"message": "Invalid user id provided"}), 400

    error, message = add_po(
        db=db,
        user_id=user_id,
        services_data=data['services']
    )
    if error:
        return jsonify({"message": message}), 400

    db.commit()

    return jsonify({"message": message})


@po_controller.route('/update', methods=['POST'])
def update_purchase_order():
    if not authenticated():
        return jsonify({"message": "Not authorized!"}), 401

    is_admin = session['user'][UserColumns.IS_ADMIN.value]
    if not is_admin:
        return jsonify({"message": "Not authorized!"}), 401

    data = request.get_json()

    if not data:
        return jsonify({"message": "No data provided"})

    if not data.get('userId'):
        return jsonify({"message": "Missing user id in data"})

    if not data.get('services'):
        return jsonify({"message": "Missing services data"})

    db = sqlite.DatabaseService()

    user_id = int(data['userId'])
    check_user_query = "SELECT * FROM users WHERE id = ?"
    result = db.run_query(check_user_query, (user_id,))
    if not result:
        return jsonify({"message": "Invalid user id"})

    print(data['services'])
    error, message = update_po(
        db=db,
        user_id=user_id,
        services_data=data['services']
    )
    if error:
        return jsonify({"message": message}), 400

    db.commit()

    return jsonify({
        "message": message
    })


@po_controller.route('/get/<id>', methods=['GET'])
def get_purchase_order(id):
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

    error, result = get_po(db, user_id=user_id)
    if error:
        return jsonify({"message": result}), 400

    return jsonify({
        "message": "Purchase order data",
        "data": {
            "userId": user_id,
            "services": result
        }
    })
