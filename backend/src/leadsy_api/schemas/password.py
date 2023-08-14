from pydantic import BaseModel, ConfigDict, EmailStr, model_validator
from pydantic.alias_generators import to_camel


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

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
