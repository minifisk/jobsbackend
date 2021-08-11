""" Utils for token management """
# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework_jwt.settings import api_settings

# App imports

# Generating a token manually, more information here: https://jpadilla.github.io/django-rest-framework-jwt/
# Potentially need to implement this, saving the link for later in that case: https://stackoverflow.com/questions/41623751/token-creation-with-rest-framework-jwt
def manually_generate_auth_token(user_model):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user_model)
    token = jwt_encode_handler(payload)

    return token
