CREATE TABLE IF NOT EXISTS unit_costs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource_name TEXT NOT NULL,
    resource_description TEXT NOT NULL,
    profit_margin INTEGER NOT NULL,
    unit_cost REAL NOT NULL,
    unit_cost_margin REAL NOT NULL,
    remarks TEXT
);