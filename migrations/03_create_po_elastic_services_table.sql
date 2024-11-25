CREATE TABLE IF NOT EXISTS po_elastic_services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    vcpus INTEGER NOT NULL,
    ram INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    rate_per_ecs REAL NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES po_users(id)
);
