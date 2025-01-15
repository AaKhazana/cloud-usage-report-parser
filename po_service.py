import sqlite
from enum import Enum


class ElasticService(Enum):
    ID = 0
    SERVICE_NAME = 1
    VCPUS = 2
    RAM = 3
    QUANTITY = 4
    RATE_PER_ECS = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class StorageService(Enum):
    ID = 0
    SERVICE_NAME = 1
    TYPE = 2
    GBS = 3
    DURATION = 4
    PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class DrService(Enum):
    ID = 0
    SERVICE_NAME = 1
    TYPE = 2
    QUANTITY = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class ContainerService(Enum):
    ID = 0
    SERVICE_NAME = 1
    DESCRIPTION = 2
    VCPU_QTY = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class ContainerServiceWorker(Enum):
    ID = 0
    SERVICE_NAME = 1
    DESCRIPTION = 2
    VCPU_QTY = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class SecurityService(Enum):
    ID = 0
    SERVICE_NAME = 1
    SERVICE_TYPE = 2
    DESCRIPTION = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class DatabaseService(Enum):
    ID = 0
    SERVICE_NAME = 1
    TYPE = 2
    QUANTITY = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class NetworkService(Enum):
    ID = 0
    SERVICE_NAME = 1
    TYPE = 2
    QUANTITY = 3
    DURATION = 4
    MONTHLY_PRICE = 5
    USER_ID = 6
    CREATED_AT = 7
    UPDATED_AT = 8


class ValueAddedService(Enum):
    ID = 0
    SERVICE_NAME = 1
    PRICE = 2
    USER_ID = 3
    CREATED_AT = 4
    UPDATED_AT = 5
    QUANTITY = 6


def get_po(db: sqlite.DatabaseService, user_id):
    if not user_id:
        return (True, "User ID not provided")

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

    services = []
    if isinstance(elastic_services, list) and len(elastic_services) > 0:
        data = []
        for elastic_service in elastic_services:
            data.append({
                "id": elastic_service[ElasticService.ID.value],
                "serviceName": elastic_service[ElasticService.SERVICE_NAME.value],
                "vCPUs": elastic_service[ElasticService.VCPUS.value],
                "ram": elastic_service[ElasticService.RAM.value],
                "quantity": elastic_service[ElasticService.QUANTITY.value],
                "rate": elastic_service[ElasticService.RATE_PER_ECS.value],
                "createdAt": elastic_service[ElasticService.CREATED_AT.value],
                "updatedAt": elastic_service[ElasticService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "elasticService",
            "data": data
        })
    if isinstance(storage_services, list) and len(storage_services) > 0:
        data = []
        for storage_service in storage_services:
            data.append({
                "id": storage_service[StorageService.ID.value],
                "serviceName": storage_service[StorageService.SERVICE_NAME.value],
                "type": storage_service[StorageService.TYPE.value],
                "gbs": storage_service[StorageService.GBS.value],
                "duration": storage_service[StorageService.DURATION.value],
                "price": storage_service[StorageService.PRICE.value],
                "createdAt": storage_service[StorageService.CREATED_AT.value],
                "updatedAt": storage_service[StorageService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "storageService",
            "data": data
        })
    if isinstance(dr_services, list) and len(dr_services) > 0:
        data = []
        for dr_service in dr_services:
            data.append({
                "id": dr_service[DrService.ID.value],
                "serviceName": dr_service[DrService.SERVICE_NAME.value],
                "type": dr_service[DrService.TYPE.value],
                "quantity": dr_service[DrService.QUANTITY.value],
                "duration": dr_service[DrService.DURATION.value],
                "monthlyPrice": dr_service[DrService.MONTHLY_PRICE.value],
                "createdAt": dr_service[DrService.CREATED_AT.value],
                "updatedAt": dr_service[DrService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "drService",
            "data": data
        })
    if isinstance(container_services, list) and len(container_services) > 0:
        data = []
        for container_service in container_services:
            data.append({
                "id": container_service[ContainerService.ID.value],
                "serviceName": container_service[ContainerService.SERVICE_NAME.value],
                "description": container_service[ContainerService.DESCRIPTION.value],
                "vcpuQty": container_service[ContainerService.VCPU_QTY.value],
                "duration": container_service[ContainerService.DURATION.value],
                "monthlyPrice": container_service[ContainerService.MONTHLY_PRICE.value],
                "createdAt": container_service[ContainerService.CREATED_AT.value],
                "updatedAt": container_service[ContainerService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "containerServices",
            "data": data
        })
    if isinstance(container_service_workers, list) and len(container_service_workers) > 0:
        data = []
        for container_service_worker in container_service_workers:
            data.append({
                "id": container_service_worker[ContainerServiceWorker.ID.value],
                "serviceName": container_service_worker[ContainerServiceWorker.SERVICE_NAME.value],
                "description": container_service_worker[ContainerServiceWorker.DESCRIPTION.value],
                "vcpuQty": container_service_worker[ContainerServiceWorker.VCPU_QTY.value],
                "duration": container_service_worker[ContainerServiceWorker.DURATION.value],
                "monthlyPrice": container_service_worker[ContainerServiceWorker.MONTHLY_PRICE.value],
                "createdAt": container_service_worker[ContainerServiceWorker.CREATED_AT.value],
                "updatedAt": container_service_worker[ContainerServiceWorker.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "containerServiceWorker",
            "data": data
        })
    if isinstance(security_services, list) and len(security_services) > 0:
        data = []
        for security_service in security_services:
            data.append({
                "id": security_service[SecurityService.ID.value],
                "serviceName": security_service[SecurityService.SERVICE_NAME.value],
                "type": security_service[SecurityService.SERVICE_TYPE.value],
                "description": security_service[SecurityService.DESCRIPTION.value],
                "duration": security_service[SecurityService.DURATION.value],
                "monthlyPrice": security_service[SecurityService.MONTHLY_PRICE.value],
                "createdAt": security_service[SecurityService.CREATED_AT.value],
                "updatedAt": security_service[SecurityService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "securityServices",
            "data": data
        })
    if isinstance(database_services, list) and len(database_services) > 0:
        data = []
        for database_service in database_services:
            data.append({
                "id": database_service[DatabaseService.ID.value],
                "serviceName": database_service[DatabaseService.SERVICE_NAME.value],
                "type": database_service[DatabaseService.TYPE.value],
                "qty": database_service[DatabaseService.QUANTITY.value],
                "duration": database_service[DatabaseService.DURATION.value],
                "monthlyPrice": database_service[DatabaseService.MONTHLY_PRICE.value],
                "createdAt": database_service[DatabaseService.CREATED_AT.value],
                "updatedAt": database_service[DatabaseService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "databaseServices",
            "data": data
        })
    if isinstance(network_services, list) and len(network_services) > 0:
        data = []
        for network_service in network_services:
            data.append({
                "id": network_service[NetworkService.ID.value],
                "serviceName": network_service[NetworkService.SERVICE_NAME.value],
                "type": network_service[NetworkService.TYPE.value],
                "qty": network_service[NetworkService.QUANTITY.value],
                "duration": network_service[NetworkService.DURATION.value],
                "monthlyPrice": network_service[NetworkService.MONTHLY_PRICE.value],
                "createdAt": network_service[NetworkService.CREATED_AT.value],
                "updatedAt": network_service[NetworkService.UPDATED_AT.value]
            })
        services.append({
            "serviceName": "networkServices",
            "data": data
        })
    if isinstance(value_added_services, list) and len(value_added_services) > 0:
        data = []
        for value_added_service in value_added_services:
            data.append({
                "serviceName": value_added_service[ValueAddedService.SERVICE_NAME.value],
                "price": value_added_service[ValueAddedService.PRICE.value],
                "qty": value_added_service[ValueAddedService.QUANTITY.value]
            })
        services.append({
            "serviceName": "valueAddedServices",
            "data": data
        })

    return (False, services)


def add_po(db: sqlite.DatabaseService, user_id: int, services_data):
    """
    Add Purchase Order
    """
    if not services_data:
        return (True, "No service data provided")

    for service in services_data:
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
                    'ecs',
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
            ns_data = service['data']
            for ns in ns_data:
                insert_ns_query = """
                INSERT INTO po_database_services (
                    service_name,
                    type,
                    quantity,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_ns_query, (
                    ns['serviceName'],
                    ns['type'],
                    ns['qty'],
                    ns['duration'],
                    ns['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'networkServices':
            ns_data = service['data']
            for ns in ns_data:
                insert_ns_query = """
                INSERT INTO po_network_services (
                    service_name,
                    type,
                    quantity,
                    duration,
                    monthly_price,
                    user_id
                ) VALUES (?, ?, ?, ?, ?, ?)"""
                db.run_query(insert_ns_query, (
                    ns['serviceName'],
                    ns['type'],
                    ns['qty'],
                    ns['duration'],
                    ns['monthlyPrice'],
                    user_id
                ))
        elif service['serviceName'] == 'valueAddedServices':
            vas_data = service['data']
            for vas in vas_data:
                insert_vas_query = """
                    INSERT INTO po_value_added_services (
                        service_name,
                        price,
                        quantity,
                        user_id
                    ) VALUES (?, ?, ?, ?)
                """
                db.run_query(
                    insert_vas_query,
                    (
                        vas['serviceName'],
                        vas['price'],
                        vas['qty'],
                        user_id,
                    )
                )

    return (False, "PO added successfully")


def update_po(db: sqlite.DatabaseService, user_id: int, services_data):
    if not services_data:
        return (True, "No service data provided")

    for service in services_data:
        if service['serviceName'] == 'elasticService':
            ecs_data = service['data']
            for ecs in ecs_data:
                if ecs.get('id'):
                    ecs_id = int(ecs['id'])
                    get_ecs_query = "SELECT * FROM po_elastic_services where id = ? and user_id = ?"
                    result = db.run_query(get_ecs_query, (ecs_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing elastic service entry with id: {ecs_id} and user_id: {user_id}")

                    old_ecs = result[0]
                    update_ecs_query = """
                        UPDATE po_elastic_services
                        SET
                            service_name = ?,
                            vcpus = ?,
                            ram = ?,
                            quantity = ?,
                            rate_per_ecs = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_ecs_query,
                        (
                            'ecs',
                            ecs.get('vCPUs', old_ecs[ElasticService.VCPUS.value]),
                            ecs.get('ram', old_ecs[ElasticService.RAM.value]),
                            ecs.get('quantity', old_ecs[ElasticService.QUANTITY.value]),
                            ecs.get('rate', old_ecs[ElasticService.RATE_PER_ECS.value]),
                            ecs_id,
                            user_id
                        )
                    )
                else:
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
                        'ecs',
                        ecs['vCPUs'],
                        ecs['ram'],
                        ecs['quantity'],
                        ecs['rate'],
                        user_id
                    ))
        elif service['serviceName'] == 'storageService':
            ss_data = service['data']
            for ss in ss_data:
                if ss.get('id'):
                    ss_id = int(ss['id'])
                    get_ss_query = "SELECT * FROM po_storage_services where id = ? and user_id = ?"
                    result = db.run_query(get_ss_query, (ss_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing storage service entry with id: {ss_id} and user_id: {user_id}")

                    old_ss = result[0]
                    update_ss_query = """
                        UPDATE po_storage_services
                        SET
                            service_name = ?,
                            type = ?,
                            gbs = ?,
                            duration = ?,
                            price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_ss_query,
                        (
                            ss.get('serviceName', old_ss[StorageService.SERVICE_NAME.value]),
                            ss.get('type', old_ss[StorageService.TYPE.value]),
                            ss.get('gbs', old_ss[StorageService.GBS.value]),
                            ss.get('duration', old_ss[StorageService.DURATION.value]),
                            ss.get('price', old_ss[StorageService.PRICE.value]),
                            ss_id,
                            user_id
                        )
                    )
                else:
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
                if dr.get('id'):
                    dr_id = int(dr['id'])
                    get_dr_query = "SELECT * FROM po_dr_services where id = ? and user_id = ?"
                    result = db.run_query(get_dr_query, (dr_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing dr service entry with id: {dr_id} and user_id: {user_id}")

                    old_dr = result[0]
                    update_dr_query = """
                        UPDATE po_dr_services
                        SET
                            service_name = ?,
                            type = ?,
                            quantity = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_dr_query,
                        (
                            dr.get('serviceName', old_dr[DrService.SERVICE_NAME.value]),
                            dr.get('type', old_dr[DrService.TYPE.value]),
                            dr.get('quantity', old_dr[DrService.QUANTITY.value]),
                            dr.get('duration', old_dr[DrService.DURATION.value]),
                            dr.get('monthlyPrice', old_dr[DrService.MONTHLY_PRICE.value]),
                            dr_id,
                            user_id
                        )
                    )
                else:
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
                if cs.get('id'):
                    cs_id = int(cs['id'])
                    get_cs_query = "SELECT * FROM po_container_services where id = ? and user_id = ?"
                    result = db.run_query(get_cs_query, (cs_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing container service entry with id: {cs_id} and user_id: {user_id}")

                    old_cs = result[0]
                    update_cs_query = """
                        UPDATE po_container_services
                        SET
                            service_name = ?,
                            description = ?,
                            vcpu_qty = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_cs_query,
                        (
                            cs.get('serviceName', old_cs[ContainerService.SERVICE_NAME.value]),
                            cs.get('description', old_cs[ContainerService.DESCRIPTION.value]),
                            cs.get('vcpuQty', old_cs[ContainerService.VCPU_QTY.value]),
                            cs.get('duration', old_cs[ContainerService.DURATION.value]),
                            cs.get('monthlyPrice', old_cs[ContainerService.MONTHLY_PRICE.value]),
                            cs_id,
                            user_id
                        )
                    )
                else:
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
                if csw.get('id'):
                    csw_id = int(csw['id'])
                    get_csw_query = "SELECT * FROM po_container_service_workers where id = ? and user_id = ?"
                    result = db.run_query(get_csw_query, (csw_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing container service worker entry with id: {csw_id} and user_id: {user_id}")

                    old_csw = result[0]
                    update_csw_query = """
                        UPDATE po_container_service_workers
                        SET
                            service_name = ?,
                            description = ?,
                            vcpu_qty = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_csw_query,
                        (
                            csw.get('serviceName', old_csw[ContainerService.SERVICE_NAME.value]),
                            csw.get('description', old_csw[ContainerService.DESCRIPTION.value]),
                            csw.get('vcpuQty', old_csw[ContainerService.VCPU_QTY.value]),
                            csw.get('duration', old_csw[ContainerService.DURATION.value]),
                            csw.get('monthlyPrice', old_csw[ContainerService.MONTHLY_PRICE.value]),
                            csw_id,
                            user_id
                        )
                    )
                else:
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
                if ss.get('id'):
                    ss_id = int(ss['id'])
                    get_ss_query = "SELECT * FROM po_security_services where id = ? and user_id = ?"
                    result = db.run_query(get_ss_query, (ss_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing security service entry with id: {ss_id} and user_id: {user_id}")

                    old_ss = result[0]
                    update_ss_query = """
                        UPDATE po_security_services
                        SET
                            service_name = ?,
                            service_type = ?,
                            description = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_ss_query,
                        (
                            ss.get('serviceName', old_ss[SecurityService.SERVICE_NAME.value]),
                            ss.get('type', old_ss[SecurityService.SERVICE_TYPE.value]),
                            ss.get('description', old_ss[SecurityService.DESCRIPTION.value]),
                            ss.get('duration', old_ss[SecurityService.DURATION.value]),
                            ss.get('monthlyPrice', old_ss[SecurityService.MONTHLY_PRICE.value]),
                            ss_id,
                            user_id
                        )
                    )
                else:
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
            ns_data = service['data']
            for ns in ns_data:
                if ns.get('id'):
                    dbs_id = int(ns['id'])
                    get_dbs_query = "SELECT * FROM po_database_services where id = ? and user_id = ?"
                    result = db.run_query(get_dbs_query, (dbs_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing database service entry with id: {dbs_id} and user_id: {user_id}")

                    old_dbs = result[0]
                    update_dbs_query = """
                        UPDATE po_database_services
                        SET
                            service_name = ?,
                            type = ?,
                            quantity = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_dbs_query,
                        (
                            ns.get('serviceName', old_dbs[DatabaseService.SERVICE_NAME.value]),
                            ns.get('type', old_dbs[DatabaseService.TYPE.value]),
                            ns.get('qty', old_dbs[DatabaseService.QUANTITY.value]),
                            ns.get('duration', old_dbs[DatabaseService.DURATION.value]),
                            ns.get('monthlyPrice', old_dbs[DatabaseService.MONTHLY_PRICE.value]),
                            dbs_id,
                            user_id
                        )
                    )
                else:
                    insert_ns_query = """
                    INSERT INTO po_database_services (
                        service_name,
                        type,
                        quantity,
                        duration,
                        monthly_price,
                        user_id
                    ) VALUES (?, ?, ?, ?, ?, ?)"""
                    db.run_query(insert_ns_query, (
                        ns['serviceName'],
                        ns['type'],
                        ns['qty'],
                        ns['duration'],
                        ns['monthlyPrice'],
                        user_id
                    ))
        elif service['serviceName'] == 'networkServices':
            ns_data = service['data']
            for ns in ns_data:
                if ns.get('id'):
                    vas_id = int(ns['id'])
                    get_vas_query = "SELECT * FROM po_network_services where id = ? and user_id = ?"
                    result = db.run_query(get_vas_query, (vas_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing network service entry with id: {vas_id} and user_id: {user_id}")

                    old_vas = result[0]
                    update_vas_query = """
                        UPDATE po_network_services
                        SET
                            service_name = ?,
                            type = ?,
                            quantity = ?,
                            duration = ?,
                            monthly_price = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_vas_query,
                        (
                            ns.get('serviceName', old_vas[ContainerService.SERVICE_NAME.value]),
                            ns.get('type', old_vas[ContainerService.DESCRIPTION.value]),
                            ns.get('qty', old_vas[ContainerService.VCPU_QTY.value]),
                            ns.get('duration', old_vas[ContainerService.DURATION.value]),
                            ns.get('monthlyPrice', old_vas[ContainerService.MONTHLY_PRICE.value]),
                            vas_id,
                            user_id
                        )
                    )
                else:
                    insert_ns_query = """
                    INSERT INTO po_network_services (
                        service_name,
                        type,
                        quantity,
                        duration,
                        monthly_price,
                        user_id
                    ) VALUES (?, ?, ?, ?, ?, ?)"""
                    db.run_query(insert_ns_query, (
                        ns['serviceName'],
                        ns['type'],
                        ns['qty'],
                        ns['duration'],
                        ns['monthlyPrice'],
                        user_id
                    ))
        elif service['serviceName'] == 'valueAddedServices':
            vas_data = service['data']
            for vas in vas_data:
                if vas.get('id'):
                    vas_id = int(vas['id'])
                    get_vas_query = "SELECT * FROM po_value_added_services where id = ? and user_id = ?"
                    result = db.run_query(get_vas_query, (vas_id, user_id))
                    if not result:
                        # TODO: might need to change the following to a continue statement
                        return (True, f"Missing value added service entry with id: {vas_id} and user_id: {user_id}")

                    old_vas = result[0]
                    update_vas_query = """
                        UPDATE po_value_added_services
                        SET
                            price = ?,
                            quantity = ?
                        WHERE
                            id = ? AND user_id = ?
                    """
                    db.run_query(
                        update_vas_query,
                        (
                            vas.get('price', old_vas[ValueAddedService.PRICE.value]),
                            vas.get('qty', old_vas[ValueAddedService.QUANTITY.value]),
                            vas_id,
                            user_id
                        )
                    )
                else:
                    insert_vas_query = """
                        INSERT INTO po_value_added_services (
                            service_name,
                            price,
                            quantity,
                            user_id
                        ) VALUES (?, ?, ?, ?)
                    """
                    db.run_query(
                        insert_vas_query,
                        (
                            vas['serviceName'],
                            vas['price'],
                            vas['qty'],
                            user_id,
                        )
                    )

    return (False, "PO updated successfully")
