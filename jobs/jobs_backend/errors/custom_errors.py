# Core Django imports

# Third-party imports

# App imports


class Error(Exception):
    def __init__(self, message=""):
        if not hasattr(self, "message"):
            self.message = message

    def __str__(self):
        return repr(self.message)


###############
# User Errors #
###############
class EmailAddressAlreadyExistsError(Error):
    message = "There is already an account associated with this email address!"
    internal_error_code = 40902
