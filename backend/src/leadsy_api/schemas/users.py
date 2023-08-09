from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel


class UserCreate(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    full_name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=8)
