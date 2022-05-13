from src.features.common.response_handlers import success_response
from src.features.common.sanitizer import sanitize_request_body

from ..checkpoint.model import Checkpoint
from .model import Segment


def get_handler():
    return success_response(Segment.fetch())


@sanitize_request_body()
def create_handler(request_body):
    return success_response(Segment.insert(request_body))


@sanitize_request_body("uuid")
def update_handler(request_body, uuid):
    return success_response(Segment.alter(uuid, request_body))


def delete_handler(uuid):
    return success_response(Segment.remove(uuid))
