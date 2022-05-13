from ...common.response_handlers import success_response
from ...common.sanitizer import sanitize_request_body
from .model import Checkpoint


def get_handler():
    return success_response(Checkpoint.fetch())


@sanitize_request_body()
def create_handler(request_body):
    return success_response(Checkpoint.insert(request_body))


@sanitize_request_body("uuid")
def update_handler(request_body, uuid):
    return success_response(Checkpoint.alter(uuid, request_body))


def delete_handler(uuid):
    return success_response(Checkpoint.remove(uuid))
