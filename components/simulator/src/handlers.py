import json
from locust import events

# JSON template for successful and failed requests
OK_TEMPLATE = '{"request_type":"%s", "name":"%s", "result":"%s", ' \
              '"response_time":"%s", "response_length":"%s", "other":%s}'

ERR_TEMPLATE = '{"request_type":"%s", "name":"%s", "result":"%s", ' \
               '"response_time":"%s", "exception":"%s", "other":%s}'

@events.request.add_listener
def debug_success_handler(request_type, name, response_time, exception, context, response_length, **kwargs):
    """Handles successful requests and logs statistics.

    Args:
        request_type (str): The type of the request (e.g., GET, POST).
        name (str): The request name.
        response_time (float): Response time in milliseconds.
        exception (Exception | None): Exception object if an error occurred.
        context (dict): Context information.
        response_length (int): The length of the response.
        **kwargs: Additional request metadata.
    """
    if exception is None:
        print(OK_TEMPLATE % (request_type, name, "OK", response_time, response_length, json.dumps(kwargs)))


@events.request.add_listener
def debug_failure_handler(request_type, name, response_time, exception, context, response_length, **kwargs):
    """ additional request failure handler to log statistics """
    if exception is not None:
        print(ERR_TEMPLATE % (request_type, name, "ERR", response_time, exception, json.dumps(kwargs)))
