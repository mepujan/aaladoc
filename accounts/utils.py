import uuid

def generateUUID():
    code = str(uuid.uuid4()).replace('-','')[:10]
    return code