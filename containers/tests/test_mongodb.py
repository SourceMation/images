import pytest
import subprocess
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

MONGODB_URI = "mongodb://admin:admin@localhost:27017/"

def test_mongodb_installed():
    result = subprocess.run(['mongod', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert result.returncode == 0, "MongoDB is not installed or mongod command is not found."
    assert "db version" in result.stdout, "MongoDB version output does not contain expected string."

def test_mongodb_connection():
    try:
        client = MongoClient(MONGODB_URI)
        client.admin.command('ping')
    except ConnectionFailure:
        pytest.fail("Failed to connect to MongoDB server.")
    finally:
        client.close()

def test_mongodb_insert_find():
    client = MongoClient(MONGODB_URI)
    db = client.test_db
    collection = db.test_collection
    
    try:
        insert_result = collection.insert_one({"name": "test_name", "value": "test_value"})
        assert insert_result.acknowledged == True, "Failed to insert document into MongoDB."

        document = collection.find_one({"name": "test_name"})
        assert document is not None, "Failed to find inserted document in MongoDB."
        assert document["value"] == "test_value", f"Expected 'test_value', got {document['value']}"
    except OperationFailure:
        pytest.fail("Operation failed due to lack of permissions.")
    finally:
        client.close()

def test_mongodb_update():
    client = MongoClient(MONGODB_URI)
    db = client.test_db
    collection = db.test_collection
    
    try:
        update_result = collection.update_one({"name": "test_name"}, {"$set": {"value": "updated_value"}})
        assert update_result.modified_count == 1, "Failed to update document in MongoDB."

        document = collection.find_one({"name": "test_name"})
        assert document["value"] == "updated_value", f"Expected 'updated_value', got {document['value']}"
    except OperationFailure:
        pytest.fail("Update operation failed due to lack of permissions.")
    finally:
        client.close()

def test_mongodb_delete():
    client = MongoClient(MONGODB_URI)
    db = client.test_db
    collection = db.test_collection
    
    try:
        delete_result = collection.delete_one({"name": "test_name"})
        assert delete_result.deleted_count == 1, "Failed to delete document from MongoDB."

        document = collection.find_one({"name": "test_name"})
        assert document is None, "Document still exists after deletion in MongoDB."
    except OperationFailure:
        pytest.fail("Delete operation failed due to lack of permissions.")
    finally:
        client.close()

def test_mongodb_drop_collection():
    client = MongoClient(MONGODB_URI)
    db = client.test_db
    collection = db.test_collection
    
    try:
        collection.insert_one({"name": "drop_test"})

        assert "test_collection" in db.list_collection_names(), "Collection does not exist before dropping."

        db.drop_collection("test_collection")

        assert "test_collection" not in db.list_collection_names(), "Collection still exists after drop operation."
    except OperationFailure:
        pytest.fail("Drop operation failed due to lack of permissions.")
    finally:
        client.close()
