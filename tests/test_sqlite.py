# tests/test_sqlite.py
from sqlite import DatabaseService
import pytest
import sys
import os
# add the path to the sqlite.py file
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def db():
    # Setup: Create a temporary database
    db = DatabaseService(':memory:')
    yield db
    # Teardown: Close the database connection
    db.conn.close()


def test_run_query_select(db):
    # Arrange: Create a table and insert data
    db.run_query(
        'CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    db.run_query('INSERT INTO test (name) VALUES (?)', ('Alice',))
    db.commit()

    # Act: Run a SELECT query
    result = db.run_query('SELECT * FROM test')

    # Assert: Verify the result
    assert len(result) == 1
    assert result[0][1] == 'Alice'


def test_run_query_insert(db):
    # Act: Run an INSERT query
    db.run_query(
        'CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    last_row_id = db.run_query('INSERT INTO test (name) VALUES (?)', ('Bob',))

    # Assert: Verify the last row ID
    assert last_row_id == 1


def test_run_query_update(db):
    db.run_query(
        'CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    db.run_query('INSERT INTO test (name) VALUES (?)', ('Alice',))
    db.commit()
    db.run_query('UPDATE test SET name = ? WHERE id = ?', ('Bob', 1))
    db.commit()
    result = db.run_query('SELECT * FROM test')
    assert len(result) == 1
    assert result[0][1] == 'Bob'


def test_run_query_delete(db):
    db.run_query(
        'CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)')
    db.commit()
    db.run_query('INSERT INTO test (name) VALUES (?)', ('Alice',))
    db.commit()
    db.run_query('DELETE FROM test WHERE id = ?', (1,))
    db.commit()
    result = db.run_query('SELECT * FROM test')
    assert len(result) == 0


def test_run_migration(db):
    db.run_migration('migrations/00_create_unit_cost_table.sql')
    db.commit()
    result = db.run_query('SELECT * FROM unit_costs')
    assert len(result) == 0

def test_run_migrations_from_folder(db):
    db.run_migrations_from_folder('migrations')
    result = db.run_query('SELECT * FROM unit_costs')
    assert len(result) == 16
