from flask import Blueprint, jsonify, request
import sqlite
from utils import validate_po_data

po_controller = Blueprint('po_controller', __name__)


@po_controller.route('/get', methods=['GET'])
def get_po():
    db = sqlite.DatabaseService()
    query = "SELECT * FROM po_users"
    result = db.run_query(query)
    if not result:
        return jsonify({"error": "No POs found"}), 404
    
    response = []
    for po in result:
        po_data = {
            'id': po[0],
            'name': po[1],
            'email': po[2],
            'ntn_number': po[3],
            'address': po[4],
            'created_at': po[5],
            'updated_at': po[6]
        }
        response.append(po_data)
    return jsonify({"message": "List of POs", "data": response})

# TODO: get po by id


@po_controller.route('/get/<id>', methods=['GET'])
def get_po_by_id(id):
    db = sqlite.DatabaseService()
    query = "SELECT * FROM po_users WHERE id = ?"
    result = db.run_query(query, (id,))
    print(result)
    if not result:
        return jsonify({"error": "PO not found"}), 404
    
    user_id = result[0][0]
    query = "SELECT * FROM po_elastic_services WHERE user_id = ?"
    elastic_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_storage_services WHERE user_id = ?"
    storage_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_dr_services WHERE user_id = ?"
    dr_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_container_services WHERE user_id = ?"
    container_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_container_service_workers WHERE user_id = ?"
    container_service_workers = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_security_services WHERE user_id = ?"
    security_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_database_services WHERE user_id = ?"
    database_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_network_services WHERE user_id = ?"
    network_services = db.run_query(query, (user_id,))
    query = "SELECT * FROM po_value_added_services WHERE user_id = ?"
    value_added_services = db.run_query(query, (user_id,))

    response = {
        "user-info": {
            "id": result[0][0],
            "name": result[0][1],
            "email": result[0][2],
            "ntn_number": result[0][3],
            "address": result[0][4],
            "created_at": result[0][5],
            "updated_at": result[0][6]
        },
        "services": []
    }
    if isinstance(elastic_services, list) and len(elastic_services) > 0:
        data = []
        for elastic_service in elastic_services:
            data.append({
                "id": elastic_service[0],
                "serviceName": elastic_service[1],
                "vCPUs": elastic_service[2],
                "ram": elastic_service[3],
                "quantity": elastic_service[4],
                "rate": elastic_service[5],
                "created_at": elastic_service[6],
                "updated_at": elastic_service[7]
            })
        response["services"].append({
            "serviceName": "elasticService",
            "data": data
        })
    if isinstance(storage_services, list) and len(storage_services) > 0:
        data = []
        for storage_service in storage_services:
            data.append({
                "id": storage_service[0],
                "serviceName": storage_service[1],
                "type": storage_service[2],
                "gbs": storage_service[3],
                "duration": storage_service[4],
                "price": storage_service[5],
                "created_at": storage_service[6],
                "updated_at": storage_service[7]
            })
        response["services"].append({
            "serviceName": "storageService",
            "data": data
        })
    if isinstance(dr_services, list) and len(dr_services) > 0:
        data = []
        for dr_service in dr_services:
            data.append({
                "id": dr_service[0],
                "serviceName": dr_service[1],
                "type": dr_service[2],
                "quantity": dr_service[3],
                "duration": dr_service[4],
                "monthlyPrice": dr_service[5],
                "created_at": dr_service[6],
                "updated_at": dr_service[7]
            })
        response["services"].append({
            "serviceName": "drService",
            "data": data
        })
    if isinstance(container_services, list) and len(container_services) > 0:
        data = []
        for container_service in container_services:
            data.append({
                "id": container_service[0],
                "serviceName": container_service[1],
                "description": container_service[2],
                "vcpuQty": container_service[3],
                "duration": container_service[4],
                "monthlyPrice": container_service[5],
                "created_at": container_service[6],
                "updated_at": container_service[7]
            })
        response["services"].append({
            "serviceName": "containerServices",
            "data": data
        })
    if isinstance(container_service_workers, list) and len(container_service_workers) > 0:
        data = []
        for container_service_worker in container_service_workers:
            data.append({
                "id": container_service_worker[0],
                "serviceName": container_service_worker[1],
                "description": container_service_worker[2],
                "vcpuQty": container_service_worker[3],
                "duration": container_service_worker[4],
                "monthlyPrice": container_service_worker[5],
                "created_at": container_service_worker[6],
                "updated_at": container_service_worker[7]
            })
        response["services"].append({
            "serviceName": "containerServiceWorker",
            "data": data
        })
    if isinstance(security_services, list) and len(security_services) > 0:
        data = []
        for security_service in security_services:
            data.append({
                "id": security_service[0],
                "serviceName": security_service[1],
                "type": security_service[2],
                "description": security_service[3],
                "duration": security_service[4],
                "monthlyPrice": security_service[5],
                "created_at": security_service[6],
                "updated_at": security_service[7]
            })
        response["services"].append({
            "serviceName": "securityServices",
            "data": data
        })
    if isinstance(database_services, list) and len(database_services) > 0:
        data = []
        for database_service in database_services:
            data.append({
                "id": database_service[0],
                "serviceName": database_service[1],
                "type": database_service[2],
                "qty": database_service[3],
                "duration": database_service[4],
                "monthlyPrice": database_service[5],
                "created_at": database_service[6],
                "updated_at": database_service[7]
            })
        response["services"].append({
            "serviceName": "databaseServices",
            "data": data
        })
    if isinstance(network_services, list) and len(network_services) > 0:
        data = []
        for network_service in network_services:
            data.append({
                "id": network_service[0],
                "serviceName": network_service[1],
                "type": network_service[2],
                "qty": network_service[3],
                "duration": network_service[4],
                "monthlyPrice": network_service[5],
                "created_at": network_service[6],
                "updated_at": network_service[7]
            })
        response["services"].append({
            "serviceName": "networkServices",
            "data": data
        })
    if isinstance(value_added_services, list) and len(value_added_services) > 0:
        # TODO: Add value added services
        pass

    return jsonify({"message": "PO User Details", "data": response})


@po_controller.route('/add', methods=['POST'])
def add_po():
    """
    Add new Purchase Order
    """

    data = request.get_json()
    # print(data)

    if not data:
        return jsonify({"error": "No data provided"}), 400

    validation_result, validation_error = validate_po_data(data)

    if not validation_result:
        return jsonify({"error": validation_error}), 400

    db = sqlite.DatabaseService()

    insert_po_user_query = """
        INSERT INTO po_users (full_name, email, ntn_number, address) VALUES (?, ?, ?, ?)
    """

    user_id = db.run_query(
        insert_po_user_query,
        (
            data['user-info']['name'],
            data['user-info']['email'],
            data['user-info'].get('ntnNumber', None),
            data['user-info'].get('address', None)
        )
    )

    for service in data['services']:
        if service['serviceName'] == 'elasticService':
            ecs_data = service['data']
            for ecs in ecs_data:
                insert_ecs_query = """
                INSERT INTO po_elastic_services (
                    service_name,
                    vcpus,
                    ram,
                    quantity,
                    rate_per_ecs,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_ecs_query, (
                    '',
                    ecs['vCPUs'],
                    ecs['ram'],
                    ecs['quantity'],
                    ecs['rate'],
                    user_id
                ))
        elif service['serviceName'] == 'storageService':
            ss_data = service['data']
            for ss in ss_data:
                insert_ss_query = """
                INSERT INTO po_storage_services (
                    service_name,
                    type,
                    gbs,
                    duration,
                    price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)
                """
                db.run_query(insert_ss_query, (
                    ss['serviceName'],
                    ss['type'],
                    ss['gbs'],
                    ss['duration'],
                    ss['price'],
                    user_id
                ))
        elif service['serviceName'] == 'drService':
            dr_data = service['data']
            for dr in dr_data:
                insert_dr_query = """
                INSERT INTO po_dr_services (
                    service_name,
                    type,
                    quantity,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_dr_query, (
                    dr['serviceName'],
                    dr['type'],
                    dr['quantity'],
                    dr['duration'],
                    dr['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'containerServices':
            cs_data = service['data']
            for cs in cs_data:
                insert_cs_query = """
                INSERT INTO po_container_services (
                    service_name,
                    description,
                    vcpu_qty,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_cs_query, (
                    cs['serviceName'],
                    cs['description'],
                    cs['vcpuQty'],
                    cs['duration'],
                    cs['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'containerServiceWorker':
            csw_data = service['data']
            for csw in csw_data:
                insert_csw_query = """
                INSERT INTO po_container_service_workers (
                    service_name,
                    description,
                    vcpu_qty,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_csw_query, (
                    csw['serviceName'],
                    csw['description'],
                    csw['vcpuQty'],
                    csw['duration'],
                    csw['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'securityServices':
            ss_data = service['data']
            for ss in ss_data:
                insert_ss_query = """
                INSERT INTO po_security_services (
                    service_name,
                    service_type,
                    description,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_ss_query, (
                    ss['serviceName'],
                    ss['type'],
                    ss['description'],
                    ss['duration'],
                    ss['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'databaseServices':
            dbs_data = service['data']
            for dbs in dbs_data:
                insert_dbs_query = """
                INSERT INTO po_database_services (
                    service_name,
                    type,
                    quantity,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_dbs_query, (
                    dbs['serviceName'],
                    dbs['type'],
                    dbs['qty'],
                    dbs['duration'],
                    dbs['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'networkServices':
            dbs_data = service['data']
            for dbs in dbs_data:
                insert_dbs_query = """
                INSERT INTO po_network_services (
                    service_name,
                    type,
                    quantity,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_dbs_query, (
                    dbs['serviceName'],
                    dbs['type'],
                    dbs['qty'],
                    dbs['duration'],
                    dbs['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'valueAddedServices':
            # TODO: Add value added services
            pass

    db.commit()


    return jsonify({"message": "PO added successfully"})
