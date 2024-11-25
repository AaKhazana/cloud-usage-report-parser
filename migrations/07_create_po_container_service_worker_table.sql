CREATE TABLE IF NOT EXISTS po_container_service_workers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    service_name TEXT NOT NULL,
    description TEXT NOT NULL,
    vcpu_qty INTEGER NOT NULL,
    duration INTEGER NOT NULL DEFAULT 730,
    monthly_price REAL NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES po_users(id)
);
