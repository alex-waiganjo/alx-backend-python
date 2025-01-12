import logging
import datetime

# Setup logger
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class RequestLoggingMiddleware:
    """ Log user requests including timestamp,user and request path """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
       # Get user
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"User: {user} - Path {request.path} - DateTime {datetime.datetime.now()}"
        logger.info(log_message)

        response = self.get_response(request)
        return response
