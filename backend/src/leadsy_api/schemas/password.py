from pydantic import BaseModel, EmailStr, model_validator


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    email: EmailStr
    password: str
    password_confirmation: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> "ResetPasswordRequest":
        if (
            self.password is not None
            and self.password_confirmation is not None
            and self.password != self.password_confirmation
        ):
            raise ValueError("Passwords do not match")
        return self
