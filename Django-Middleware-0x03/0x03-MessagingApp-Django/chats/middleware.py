import logging
import datetime
from django.http import HttpResponseForbidden


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


class RestrictAccessByTimeMiddleware:
    "Restrict server access between 6pm and 9pm"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_hour = 18
        end_hour = 21

        current_hour = datetime.now.hour()
        if "/messaging_app/" in request.path: 
            if not (end_hour <= current_hour < start_hour):
                return HttpResponseForbidden("Access to the messaging app is restricted during these hours.")
        return self.get_response(request)

    
        