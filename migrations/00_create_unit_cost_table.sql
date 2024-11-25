CREATE TABLE IF NOT EXISTS unit_costs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_desc TEXT NOT NULL,
    profit_margin INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    unit_cost_margin REAL NOT NULL,
    appx_monthly_cost REAL NOT NULL,
    remarks TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);