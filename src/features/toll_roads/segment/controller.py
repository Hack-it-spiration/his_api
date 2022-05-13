from flask import current_app
from src.features.common.helpers.pagination import get_pagination_params
from src.features.common.response_handlers import success_response
from src.features.common.sanitizer import sanitize_request_body

from .model import Segment


def get_handler(url_params):
    page, page_size = get_pagination_params(
        url_params, current_app.config["DEFAULT_ITEM_PER_PAGE"]
    )
    return success_response(Segment.fetch(page, page_size))


@sanitize_request_body()
def create_handler(request_body):
    return success_response(Segment.insert(request_body))


@sanitize_request_body("uuid")
def update_handler(request_body, uuid):
    return success_response(Segment.alter(uuid, request_body))


def delete_handler(uuid):
    return success_response(Segment.remove(uuid))
