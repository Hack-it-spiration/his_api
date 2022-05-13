import werkzeug.exceptions
from werkzeug.exceptions import Conflict, Forbidden, UnprocessableEntity


class APIException(Exception):
    """Base exception for API exceptions.

    Attributes:
        status: HTTP status code.
        error: error name or message.
        detail: error detail.
    """

    def __init__(self, status, error, detail={}):
        super().__init__(error)
        self.status = status
        self.error = error
        self.detail = detail


class AlreadyExists(APIException):
    """Already exists exception.

    Raised when trying to save a document with an already existing value for a
    unique field.
    """

    def __init__(self, detail={}):
        super().__init__(Conflict.code, "ALREADY_EXISTS", detail)


class MaliciousRequest(APIException):
    """Malicious request exception.

    Raised when processing a request that is malicious to the system.
    """

    def __init__(self, detail={}):
        super().__init__(Forbidden.code, "MALICIOUS_REQUEST", detail)


class InvalidUrlParam(APIException):
    """Invalid URL parameter exception.

    Raised when processing a request with a useful URL parameter that has
    a wrong type or value.
    """

    def __init__(self, detail={}):
        super().__init__(UnprocessableEntity.code, "INVALID_URL_PARAMETER", detail)


class InvalidSearchFilter(APIException):
    """Invalid search filter exception.

    Raised when processing a search request with an invalid filter key or value.
    """

    def __init__(self, detail={}):
        super().__init__(UnprocessableEntity.code, "INVALID_SEARCH_FILTER", detail)


class NotFound(werkzeug.exceptions.NotFound):
    """*404* Not found exception.

    Raised if a requested resource does not exist.
    """

    def __init__(self):
        super().__init__(response="NOT_FOUND")


class BadRequest(werkzeug.exceptions.BadRequest):
    """*400* Bad request exception.

    Raised if the server cannot handle the received request.
    """

    def __init__(self):
        super().__init__(response="BAD_REQUEST")


class UnprocessableEntity(werkzeug.exceptions.UnprocessableEntity):
    """*422* Unprocessable Entity exception.

    Raised if if the request is well formed, but the instructions are otherwise
    incorrect.
    """

    def __init__(self):
        super().__init__(response="UNPROCESSABLE_ENTITY")
