import sqlite3
import glob

# # Create a table for users
# ('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT NOT NULL,
#     email TEXT NOT NULL,
#     address TEXT NOT NULL,
#     ntn_number TEXT NOT NULL CHECK(ntn_number LIKE '%-%')
# )
# ''')

# # Create a table for ECS instances
# ('''
# CREATE TABLE IF NOT EXISTS ecs_instances (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     instance_name TEXT NOT NULL,
#     vcpus INTEGER NOT NULL,
#     memory INTEGER NOT NULL,
#     quantity INTEGER NOT NULL,
#     user_id INTEGER NOT NULL,
#     FOREIGN KEY (user_id) REFERENCES users(id)
# )
# ''')

class DatabaseService:
    def __init__(self, db_path='invoice.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
            print(exc_val)
            print(exc_tb)
        self.conn.commit()
        self.conn.close()

    def run_query(self, query, params=None):
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        self.conn.commit()
        return self.cursor.fetchall()
    

    def run_migration_from_file(self, file_path):
        with open(file_path, 'r') as file:
            migration_query = file.read()
            self.run_query(migration_query)

    def run_migrations_from_folder(self, folder_path):
        for file_path in glob.glob(folder_path + '/*.sql'):
            self.run_migration_from_file(file_path)
