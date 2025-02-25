import pytest
import subprocess
import os
import psycopg2
from psycopg2 import sql

def test_postgresql_installed():
    result = subprocess.run(['psql', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "PostgreSQL is not installed or not found in system PATH"
    assert "psql (PostgreSQL)" in result.stdout, f"Unexpected output from 'psql --version': {result.stdout}"

def test_postgresql_connection():
    try:
        connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
        connection.close()
    except Exception as e:
        pytest.fail(f"Failed to connect to PostgreSQL: {e}")

def test_create_and_drop_database():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    connection.autocommit = True
    cursor = connection.cursor()
    
    try:
        cursor.execute(sql.SQL("CREATE DATABASE test_db"))
        cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = 'test_db'"))
        assert cursor.fetchone() is not None, "Failed to create database 'test_db'"
    finally:
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS test_db"))
        cursor.close()
        connection.close()

def test_create_table_and_insert_record():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    cursor = connection.cursor()
    
    try:
        cursor.execute(sql.SQL("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(50))"))
        cursor.execute(sql.SQL("INSERT INTO test_table (name) VALUES (%s)"), ["test_name"])
        cursor.execute(sql.SQL("SELECT name FROM test_table WHERE name = %s"), ["test_name"])
        result = cursor.fetchone()
        assert result is not None and result[0] == "test_name", "Failed to insert or retrieve record from 'test_table'"
    finally:
        cursor.execute(sql.SQL("DROP TABLE IF EXISTS test_table"))
        cursor.close()
        connection.close()

def test_pg_dump():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    connection.autocommit = True
    cursor = connection.cursor()
    
    try:
        cursor.execute(sql.SQL("CREATE DATABASE test_dump_db"))
        
        dump_result = subprocess.run(
            ['pg_dump', '-U', 'postgres', 'test_dump_db', '-f', 'test_dump.sql'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        assert dump_result.returncode == 0, f"pg_dump failed: {dump_result.stderr}"
        assert os.path.exists('test_dump.sql'), "pg_dump did not create the expected dump file"
    finally:
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS test_dump_db"))
        cursor.close()
        connection.close()
        if os.path.exists('test_dump.sql'):
            os.remove('test_dump.sql')

def test_pg_restore():
    connection = psycopg2.connect(dbname="postgres", user="postgres", password="postgres", host="localhost")
    connection.autocommit = True
    cursor = connection.cursor()
    
    try:
        cursor.execute(sql.SQL("CREATE DATABASE test_restore_target_db"))

        target_conn = psycopg2.connect(dbname="test_restore_target_db", user="postgres", password="postgres", host="localhost")
        target_cursor = target_conn.cursor()
        target_cursor.execute(sql.SQL("CREATE TABLE test_table (id SERIAL PRIMARY KEY, name VARCHAR(50))"))
        target_cursor.execute(sql.SQL("INSERT INTO test_table (name) VALUES (%s)"), ["restore_test_name"])
        target_conn.commit()
        target_cursor.close()
        target_conn.close()
        
        dump_result = subprocess.run(
            ['pg_dump', '-U', 'postgres', '-Fc', 'test_restore_target_db', '-f', 'test_restore.dump'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        assert dump_result.returncode == 0, f"pg_dump failed: {dump_result.stderr}"
        
        cursor.execute(sql.SQL("CREATE DATABASE test_restore_db"))

        restore_result = subprocess.run(
            ['pg_restore', '-U', 'postgres', '-d', 'test_restore_db', 'test_restore.dump'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        assert restore_result.returncode == 0, f"pg_restore failed: {restore_result.stderr}"
        
        restore_conn = psycopg2.connect(dbname="test_restore_db", user="postgres", password="postgres", host="localhost")
        restore_cursor = restore_conn.cursor()
        restore_cursor.execute(sql.SQL("SELECT name FROM test_table WHERE name = %s"), ["restore_test_name"])
        result = restore_cursor.fetchone()
        assert result is not None and result[0] == "restore_test_name", "Failed to restore data from dump"
        restore_cursor.close()
        restore_conn.close()
    finally:
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS test_restore_db"))
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS test_restore_target_db"))
        cursor.close()
        connection.close()
        if os.path.exists('test_restore.dump'):
            os.remove('test_restore.dump')
