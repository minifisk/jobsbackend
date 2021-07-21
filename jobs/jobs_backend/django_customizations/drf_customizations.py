# Standard Library imports

# Core Django imports

# Third-party imports
from rest_framework import permissions

# App imports

"""     Custom permissions to be used for different Django-Views:
"""



class AccountCreation(permissions.BasePermission):
    """     Return True (permission granted) for POST requests (as in creating a new user account through a form).
            Return True if user is authenticated
            Return False for all other cases, as the user is not authenticated, and trying to access data
    """

    def has_permission(self, request, view):
        if (request.method == "POST") or request.user.is_authenticated:
            return True
        return False
