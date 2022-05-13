from ..common.exceptions import MaliciousRequest


def sanitize_request_body(*args, **kwargs):
    """Sanitizes a request body before being processed by the controller.

    If you decorate a controller with this, it will ensure that the request body
    received by the controller is sanitized from malicious payloads.
    Requires the controller to accept request_body as the first positional argument
    or as the kwarg associated with the key "request_body".

    Args:
        *args, **kwargs:
            Variable length argument list, arbitrary keyword arguments used to pass
            additional fields names to include in the sanitization.
    """

    def decorator(fn):
        # "_id" field has aliases defined by mongoengine ("id", "pk")
        api_managed_fields = {"_id", "id", "pk", "author", "created_at", "updated_at"}
        to_sanitize = api_managed_fields | set(args) | set(kwargs.values())

        def wrapper(*args, **kwargs):
            if args:
                body = args[0]
            else:
                body = kwargs.get("request_body")
            if body:
                for field in to_sanitize:
                    if field in body:
                        raise MaliciousRequest()

            return fn(*args, **kwargs)

        return wrapper

    return decorator
