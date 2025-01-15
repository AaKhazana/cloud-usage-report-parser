CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name CHAR(50) NOT NULL,
    email CHAR(120) NOT NULL,
    organization CHAR(120),
    address TEXT,
    ntn_number CHAR(50),
    password_hash CHAR(128) NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
