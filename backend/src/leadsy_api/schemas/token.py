from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AccessTokenResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    token_type: str
    access_token: str
