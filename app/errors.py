class UserAlreadyExistsError(Exception):
    pass


class InvalidEmailOrPasswordError(Exception):
    pass


class EmailVerificationError(Exception):
    def __init__(
        self, *args: object, timeout: bool = False, invalid_email: bool = False
    ) -> None:
        super().__init__(*args)
        self.timeout = timeout
        self.invalid_email = invalid_email


class PasswordDoesNotMatchError(Exception):
    pass


class SetDoesNotExistsError(Exception):
    pass
