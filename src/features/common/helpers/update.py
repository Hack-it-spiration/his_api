from datetime import datetime

from mongoengine.errors import FieldDoesNotExist


def update_fields(update_request_body, stored_item):
    unknown_fields = ""
    for field in update_request_body:
        try:
            stored_item[field] = update_request_body[field]
        except KeyError as e:
            unknown_fields += str(e)

    if unknown_fields:
        raise FieldDoesNotExist(unknown_fields)
    stored_item["updated_at"] = datetime.now()
