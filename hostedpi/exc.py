class HostedPiException(Exception):
    "Base class for all exceptions in the hostedpi module"


class MythicAuthenticationError(HostedPiException):
    "Exception raised when authentication fails"


class HostedPiUserError(HostedPiException):
    "Base exception for user errors, such as invalid input or configuration issues"


class HostedPiValidationError(HostedPiUserError):
    "Exception raised for validation errors, such as invalid data formats or missing required fields"


class HostedPiServerError(HostedPiException):
    "Exception raised for server errors, such as API errors or server-side issues"


class HostedPiInvalidParametersError(HostedPiServerError, HostedPiUserError):
    "Exception raised for invalid parameters in API requests or server operations"


class HostedPiNotAuthorizedError(HostedPiServerError):
    "Exception raised when the user is not authorized to perform a specific action or access a resource"


class HostedPiOutOfStockError(HostedPiServerError):
    "Exception raised when no servers with the required specification are available"


class HostedPiProvisioningError(HostedPiServerError):
    "Exception raised when an action cannot be performed because the Pi is still being provisioned"


class HostedPiNameExistsError(HostedPiServerError):
    "Exception raised when a Pi with the specified name already exists"
