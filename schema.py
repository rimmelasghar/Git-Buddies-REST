from pydantic import BaseModel, ValidationError
from typing import List, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Union[str, None] = None
    scopes: List[str] = []


class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserOut(BaseModel):
    id : int
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    

class UserIn(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None
    password: str

class UserInDB(User):
    password: str
    
class Repo(BaseModel):
    username :str
    title : str
    repolink : str
    status : bool
    

class BalanceIn(BaseModel):
    id : int
    user_id : int
    balance : int
    
class BalanceOut(BaseModel):
    id : int
    user_id : int
    balance : int

