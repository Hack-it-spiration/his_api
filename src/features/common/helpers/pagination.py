from ..exceptions import InvalidUrlParam


def page_to_slice(page, page_size):
    """Converts (page, page_size) pagination to a slice (start_index, end_index).

    Args:
        page:
            Page number (0 indexed).
        page_size:
            Page size.
    Returns:
        A tuple (start_index, end_index).
    """
    start_index = page * page_size
    end_index = start_index + page_size
    return start_index, end_index


def get_pagination_params(url_params, default_item_per_page):
    """Retrieves page and page_size from URL parameters.

    Retrieves page and page_size if provided in URL parameters, else use default
    values (page=0, page_size=ITEMS_PER_PAGE). Raises "InvalidUrlParam" if invalid
    page, page_size are provided.

    Args:
        url_params:
            A dict mapping URL parameters to their values.
    Returns:
        A tuple (page, page_size).
    """
    try:
        page = int(url_params.get("page", 0))
        page_size = int(url_params.get("pageSize", default_item_per_page))
        assert page >= 0 and page_size >= 0
        return page, page_size
    except (ValueError, AssertionError):
        raise InvalidUrlParam()
