class DomainException(Exception):
    """Base class for domain exceptions."""
    pass


class PostNotFoundException(DomainException):
    """Raised when a post is not found or not published."""
    def __init__(self, message: str = "Post not found"):
        self.message = message
        super().__init__(self.message)


class InvalidIdException(DomainException):
    """Raised when an identifier has an invalid format."""
    def __init__(self, message: str = "Invalid ID"):
        self.message = message
        super().__init__(self.message)
