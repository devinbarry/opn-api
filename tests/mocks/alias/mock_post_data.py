import uuid

test_uuid = str(uuid.uuid4())


def mock_add_item_data():
    return {"result": "saved", "uuid": str(uuid.uuid4())}


def mock_del_item_data():
    return {"status": "success", "message": "Item deleted successfully"}


def mock_import_data():
    return {"status": "success", "imported_count": 5}


def mock_reconfigure_data():
    return {"status": "success", "message": "Reconfiguration completed"}


def mock_set_data():
    return {"status": "success", "uuid": "updated_item_uuid"}


def mock_set_item_data():
    return {"status": "success", "uuid": "updated_item_uuid"}


def mock_toggle_item_data():
    return {"status": "success", "enabled": True}
