import logging
import datetime
from django.http import HttpResponseForbidden, JsonResponse


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

    
class OffensiveLanguageMiddleware:
    """
    Middleware to limit the number of messages sent by an IP address within a time window.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_message_log = {}

    def __call__(self, request):
        if request.method == "POST" and "/messaging/" in request.path:  # Adjust the path as per your app
            # Get the user's IP address
            user_ip = self.get_client_ip(request)

            # Initialize or update the IP log
            now = datetime.now()
            if user_ip not in self.ip_message_log:
                self.ip_message_log[user_ip] = []

            # Remove timestamps older than 1 minute
            one_minute_ago = now - datetime.timedelta(minutes=1)
            self.ip_message_log[user_ip] = [
                timestamp for timestamp in self.ip_message_log[user_ip]
                if timestamp > one_minute_ago
            ]

            # Check the message count within the last minute
            if len(self.ip_message_log[user_ip]) >= 5:  # Limit of 5 messages per minute
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait before sending more messages."},
                    status=429
                )

            self.ip_message_log[user_ip].append(now)
        return self.get_response(request)

    def get_client_ip(self, request):
        """
        Helper function to get the client IP address from the request.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0]
        return request.META.get("REMOTE_ADDR")


class RolePermissionMiddleware:
    """
    Middleware to restrict access to specific actions based on user roles.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Define the restricted paths or actions
        restricted_paths = ["/admin-action/", "/moderator-action/"]  # Adjust to your app's URLs

        # Check if the path is restricted
        if any(request.path.startswith(path) for path in restricted_paths):
            user = request.user
            if not user.is_authenticated or not (user.is_admin or user.groups.filter(name="moderator").exists()):
                return JsonResponse({"error": "Forbidden: You do not have the necessary permissions."}, status=403)
        return self.get_response(request)