from functools import wraps
import json
import jwt
from django.http import HttpResponse
from user_service.settings import SECRET_KEY

key = SECRET_KEY


def authorize():
    def decorator(f):
        @wraps(f)
        def decorated_function(view, *args, **kwargs):
            token = None
            if "Authorization" in view.request.headers:
                token = view.request.headers["Authorization"]
                token_padding = token[:6]
                token_value = token[6:]
                secret_key = token_padding + key
            if not token:
                return HttpResponse(
                    json.dumps({"message": "token is missing"}),
                    content_type="application/json",
                )

            try:
                data = jwt.decode(token_value, secret_key, algorithms="HS256")
                authorize.user_data = data
                responses = f(view.request, *args, **kwargs)
                return responses

            except Exception as err:
                return HttpResponse(
                    json.dumps({"error": "your token has been expired"}),
                    content_type="application/json",
                )

        return decorated_function

    return decorator
