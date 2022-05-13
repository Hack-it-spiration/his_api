from re import findall

from mongoengine.errors import DoesNotExist, FieldDoesNotExist, ValidationError
from werkzeug.exceptions import HTTPException

from ..common.exceptions import APIException, UnprocessableEntity
from .helpers.validation_errors import to_std_errors


def success_response(data):
    return {"status": 200, "data": data}


def error_response(code, error, detail={}):
    response = (
        {"status": code, "error": error, "detail": detail}
        if detail
        else {"status": code, "error": error}
    )
    return response, code


error_handlers = {
    ValidationError: lambda e: error_response(
        UnprocessableEntity.code, "VALIDATION_ERROR", to_std_errors(e.to_dict())
    ),
    DoesNotExist: lambda e: error_response(UnprocessableEntity.code, "DOES_NOT_EXIST"),
    FieldDoesNotExist: lambda e: error_response(
        UnprocessableEntity.code, "UNKNOWN_FIELD", findall("'([^']*)'", str(e))
    ),
    HTTPException: lambda e: error_response(e.code, e.response or e.description, {}),
    APIException: lambda e: error_response(e.status, e.error, e.detail),
}
