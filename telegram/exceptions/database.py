class UserNotFound(Exception):
    def __init__(self, message="User is not found") -> Exception:
        super().__init__(message)
