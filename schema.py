from pydantic import BaseModel, ValidationError
from typing import List, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class Repo(BaseModel):
    username :str
    title : str
    repolink : str
    status : bool
    
