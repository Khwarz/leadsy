from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    token: str
    email: EmailStr
    password: str
