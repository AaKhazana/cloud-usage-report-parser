import sqlite3
import glob
import re

class DatabaseService:
    def __init__(self, db_path='invoice.db'):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        self.run_query('''
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration_file TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
            print(exc_val)
            print(exc_tb)
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def run_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except Exception as e:
            raise e

        is_select = query.strip().upper().startswith('SELECT')
        if is_select:
            return self.cursor.fetchall()
        else:
            return self.cursor.lastrowid

    def run_migration(self, file_path):
        with open(file_path, 'r') as file:
            migration_query = file.read()
            self.run_query(migration_query)

    def check_migration(self, file_path):
        return self.run_query('''
            SELECT * FROM migrations WHERE migration_file = ?
        ''', (file_path,))

    def run_migrations_from_folder(self, folder_path):
        files = glob.glob(f"{folder_path}/*.sql")
        files = sorted(files, key=lambda x:float(re.findall("(\\d+)",x)[0]))
        for file in files:
            if not self.check_migration(file):
                print(f"Running migration from {file}")
                self.run_migration(file)
                self.run_query('''
                    INSERT INTO migrations (migration_file) VALUES (?)
                ''', (file,))