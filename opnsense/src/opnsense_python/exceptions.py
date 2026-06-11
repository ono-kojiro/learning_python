class OPNsenseAPIError(Exception):
    """Base exception for OPNsense API errors."""
    pass


class AuthenticationError(OPNsenseAPIError):
    """Raised when authentication fails."""
    pass


class NotFoundError(OPNsenseAPIError):
    """Raised when an API endpoint is not found."""
    pass


