from datetime import datetime, timedelta
from typing import List, Union
from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm,SecurityScopes
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import  ValidationError
from schema import  User,Token,TokenData,UserInDB,UserIn,Repo,BalanceIn,BalanceOut,UserOut
from models import loginTable,repoTable,balanceTable
from connection import session
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# openssl rand -hex 32
SECRET_KEY = "1efdb5fc051f8135b9d4be6c60949a672969219744e21067f0a5d049414ee9df"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"user": "options for user", "admin": "admins options"},
)

app = FastAPI()


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def model_to_dict(model):
    """Convert a SQLAlchemy model object to a dictionary."""
    result = {}
    for key in model.__dict__.keys():
        if not key.startswith('_'):
            result[key] = model.__dict__[key]
    return result


def get_user(username: str):
    res = session.query(loginTable).filter(loginTable.username == username).all()
    if res:
        return UserInDB(**model_to_dict(res[0]))
    else:
        return None


def authenticate_user(username: str, password: str):
    user = get_user(username)
    if user:
        if verify_password(password, user.password):
            return user
        else:
            return False
    else:
        return False


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(
    current_user: User = Security(get_current_user, scopes=["user"])
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def delete_row(MyModel, row_username: str):
    row = session.query(MyModel).filter(MyModel.username == row_username).first()
    if row:
        session.delete(row)
        session.commit()
        return {"message": "Row deleted successfully."}
    else:
        return {"message": "Row not found."}
    
def delete_row_by_id(MyModel, row_id: str):
    row = session.query(MyModel).filter(MyModel.id == row_id).first()
    if row:
        session.delete(row)
        session.commit()
        return {"message": "Row deleted successfully."}
    else:
        return {"message": "Row not found."}   
    
    
    

# Api 
    
@app.post("/token", response_model=Token,tags=["Auth"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "scopes": form_data.scopes},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=UserOut,tags=["Users"])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    user = session.query(loginTable).filter(loginTable.username == current_user.username).first()
    return UserOut(**model_to_dict(user))

@app.post("/users/add/",tags=["Users"])
async def add_user(user: UserIn, current_user: User = Security(get_current_active_user, scopes=["user"])):
    password = get_password_hash(user.password)
    new_user = loginTable(username=user.username,email=user.email,full_name=user.full_name,disabled=user.disabled,password=password)
    session.add(new_user)
    session.commit()
    return {"username":user.username}



@app.delete("/users/delete/",tags=["Users"])
def remove_user(user:UserIn,
    current_user: User = Security(get_current_active_user, scopes=["user"])
):
    res = delete_row(loginTable,user.username)
    session.commit()
    return res

@app.put("/users/update",tags=["Users"])
async def update_user(user : UserIn,current_user: User = Security(get_current_active_user, scopes=["user"])):
    res = session.query(loginTable).filter(loginTable.username == user.username).first()
    res.username,res.full_name,res.email,res.password,res.disabled = user.username,user.full_name,user.email,user.password,res.disabled
    session.commit()
    return model_to_dict(res)

@app.get("/users/all/",response_model=List[UserOut],tags=["Users"])
async def fetch_all_users(
    current_user: User = Security(get_current_active_user, scopes=["admin"])
):
    res = session.query(loginTable).filter(loginTable.disabled == False).all()
    result = [UserOut(**model_to_dict(i)) for i in res]
    return result


@app.get("/boosted/repos",tags=["Boosted Repository"])
async def get_all_boosted_repository(current_user: User = Security(get_current_active_user, scopes=["user"])):
    repos = session.query(repoTable).filter(repoTable.status != 0).all()
    if repos:
        return [model_to_dict(rep) for rep in repos]
    else:
        return []
    

@app.post("/boosted/repos",tags=["Boosted Repository"])
async def create_boosted_repository(repo : Repo,current_user: User = Security(get_current_active_user, scopes=["user"])):
    user = session.query(loginTable).filter(loginTable.username == current_user.username).first()
    repo = repoTable(user_id=user.id,status=repo.status,repolink=repo.repolink)
    session.add(repo)
    session.commit()
    return {"message":"reposity is boosted"}

@app.put("/boosted/repos/{id}",tags=["Boosted Repository"])
async def update_boosted_repository(id : int,current_user: User = Security(get_current_active_user, scopes=["user"])):
    res = session.query(repoTable).filter(repoTable.id == id).first()
    res.status = 0
    session.commit()
    return {"message":"repository status updated"}

@app.delete("/boosted/repos/{id}",tags=["Boosted Repository"])
async def delete_boosted_repository(id:int,current_user: User = Security(get_current_active_user, scopes=["user"])):
    res = delete_row_by_id(repoTable,id)
    return res

## Balance Endpoints
@app.get("/user/balance/{id}",tags=["balance"],response_model=BalanceOut)
async def get_current_user_balance(id:int,current_user: User = Security(get_current_active_user, scopes=["user"])):
    res = session.query(balanceTable).filter(balanceTable.user_id == id).first()
    if res:
        return BalanceOut(**model_to_dict(res))
    else:
        return []

@app.post("/user/balance/{id}",tags=["balance"])
async def post_current_user_balance(id:int,current_user: User = Security(get_current_active_user, scopes=["user"])):
    check = session.query(balanceTable).filter(balanceTable.user_id == id).first()
    if check:
        return {"message":"user Balance already exits"}
    else:
        user = balanceTable(user_id=id,balance=0)
        session.add(user)
        session.commit()
        return {"message":"user Balance added"}

@app.put("/user/balance/",tags=["balance"])
async def update_current_user_balance(bal:BalanceIn,current_user: User = Security(get_current_active_user, scopes=["user"])):
    res = session.query(balanceTable).filter(balanceTable.user_id == bal.user_id).first()
    res.balance = bal.balance
    session.commit()
    return {"message":"balance updated Successfully"}
    


# uncomment when using first time
# new_user = loginTable(username="admin",email="admin@admin",full_name="admin",disabled=False,password=get_password_hash("admin"))
# session.add(new_user)
# session.commit()

