class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        error_code: str = "APPLICATION_ERROR",
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code


class EmailAlreadyExistsException(AppException):
    def __init__(self):
        super().__init__(
            message="Email already registered.",
            status_code=400,
            error_code="EMAIL_ALREADY_EXISTS",
        )