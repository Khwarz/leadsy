from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AccessTokenResponse(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)

    token_type: str
    access_token: str


class RevokeAccessTokenRequest(BaseModel):
    token: str
