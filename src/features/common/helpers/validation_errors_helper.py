from re import fullmatch


STD_ERRORS_MATCHING = [
    ("Field is required", "REQUIRED_FIELD"),
    ("Field is required and cannot be empty", "REQUIRED_FIELD"),
    ("StringField only accepts string values", "INVALID_TYPE"),
    ("Only lists and tuples may be used in a list field", "INVALID_TYPE"),
    (".* could not be converted to int", "INVALID_TYPE"),
    ("GeoPointField can only accept tuples or lists of \(x, y\)", "INVALID_TYPE"),
    ("Both values .* in point must be float or int", "INVALID_TYPE"),
    ("Value .* must be a two-dimensional point", "INVALID_TYPE"),
    ("String value is too short", "INVALID_VALUE"),
    ("String value is too long", "INVALID_VALUE"),
    ("String value did not match validation regex", "INVALID_VALUE"),
    ("Value must be one of .*", "INVALID_VALUE"),
    ("Integer value is too small", "INVALID_VALUE"),
    ("Integer value is too large", "INVALID_VALUE"),
    (
        "Could not convert to UUID: badly formed hexadecimal UUID string",
        "INVALID_VALUE",
    ),
]


def to_std_errors(errors):
    print(errors)
    for field, message in errors.items():
        if not isinstance(message, str):
            errors[field] = to_std_errors(message)
            continue
        for message_regex, std_error in STD_ERRORS_MATCHING:
            if fullmatch(message_regex, message):
                errors[field] = std_error
                break
    return errors
