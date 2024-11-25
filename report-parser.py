#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import argparse
import sqlite
from utils import parse_excel_report
from po_controller import po_controller

app = Flask(__name__)
CORS(app)

app.register_blueprint(po_controller, url_prefix='/po')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'uploads')):
            os.makedirs(os.path.join(os.path.dirname(__file__), 'uploads'))
        file_path = os.path.join(os.path.dirname(
            __file__), 'uploads', file.filename)
        file.save(file_path)
        parsed_report_data = parse_excel_report(file_path)
        # delete the uploaded file
        os.remove(file_path)
        return parsed_report_data


@app.route('/unit-costs', methods=['GET'])
def get_unit_costs():
    try:
        db = sqlite.DatabaseService()
        results = db.run_query("SELECT * FROM unit_costs")

        unit_costs = []
        for row in results:
            unit_costs.append({
                "id": row[0],
                "resource_desc": row[1],
                "profit_margin": row[2],
                "unit_cost": row[3],
                "unit_cost_margin": row[4],
                "appx_monthly_cost": row[5],
                "remarks": row[6]
            })

        return jsonify({"unit_costs": unit_costs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/unit-costs', methods=['POST'])
def update_unit_costs():
    try:
        data = request.get_json()
        if not isinstance(data, list):
            return jsonify({"error": "Request body must be an array"}), 400

        if len(data) == 0:
            return jsonify({"error": "No data to update"}), 400

        db = sqlite.DatabaseService()
        updated_count = 0

        for item in data:
            if 'id' not in item:
                continue

            if len(item) <= 1:
                continue

            # Check if record exists
            result = db.run_query(
                "SELECT * FROM unit_costs WHERE id = ?", (item['id'],))
            if not result:
                continue

            unit_cost = item.get('unit_cost', result[0][3])
            unit_cost_margin = unit_cost + unit_cost * \
                (item.get('profit_margin', result[0][2]) / 100)
            appx_monthly_cost = unit_cost_margin * 730

            # Update the record
            update_query = """
                UPDATE unit_costs 
                SET resource_desc = ?,
                    profit_margin = ?,
                    unit_cost = ?,
                    unit_cost_margin = ?,
                    appx_monthly_cost = ?,
                    remarks = ?
                WHERE id = ?
            """

            db.run_query(update_query, (
                item.get('resource_desc', result[0][1]),
                item.get('profit_margin', result[0][2]),
                unit_cost,
                unit_cost_margin,
                appx_monthly_cost,
                item.get('remarks', result[0][6]),
                item['id']
            ))
            updated_count += 1

        db.commit()
        return jsonify({
            "message": f"Successfully updated {updated_count} unit costs",
            "updated_count": updated_count
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # read args
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='0.0.0.0')
    parser.add_argument('--port', type=int, default=5000)
    parser.add_argument('--debug', type=bool, default=False)
    parser.add_argument('--migrateall', type=str, default='',
                        help='run all migrations from folder')
    parser.add_argument('--migrate', type=str, default='',
                        help='run single migration file')
    args = parser.parse_args()

    if args.migrateall:
        if not os.path.exists(args.migrateall):
            print(f"Migrations folder does not exist: {args.migrateall}")
            exit(1)
        print(f"Applying all migrations from folder: {args.migrateall}")
        db = sqlite.DatabaseService()
        db.run_migrations_from_folder(args.migrateall)
        db.commit()
        exit(0)

    if args.migrate:
        db = sqlite.DatabaseService()
        print(f"Migrating from file: {args.migrate}")
        db.run_migration(args.migrate)
        db.commit()
        exit(0)

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )
