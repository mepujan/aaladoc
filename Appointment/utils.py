import uuid


def get_code():
    code = str(uuid.uuid4()).replace("-", "")[:10]
    return code
