class BlogError(Exception):
    """Custom exception for conversion errors."""
    pass

class ConversionError(Exception):
    """Custom exception for conversion errors."""
    pass

class AuthenticationError(Exception):
    """Custom exception for authentication failures"""
    pass

class RegistrationError(Exception):
    """Custom exception for registration failures"""
    pass

class ValidationError(Exception):
    """Custom exception for validation failures"""
    pass