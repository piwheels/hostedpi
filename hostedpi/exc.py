class HostedPiException(Exception):
    "Base class for all exceptions in the hostedpi module"

class MythicAuthenticationError(HostedPiException):
    "Exception raised when authentication fails"
