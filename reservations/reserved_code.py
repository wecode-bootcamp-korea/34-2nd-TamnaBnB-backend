import uuid

def reservation_code() :
    code = str(uuid.uuid4())[9:23]

    return code