from fastapi import FastAPI, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
import httpx
from models import repoTable,UserTable
import urllib
from connection import session
from schema import Repo

app = FastAPI()

client_id = "your github app client Id"
client_secret = "your github app client secret"


def model_to_dict(model):
    """Convert a SQLAlchemy model object to a dictionary."""
    result = {}
    for key in model.__dict__.keys():
        if not key.startswith('_'):
            result[key] = model.__dict__[key]
    return result

    
def delete_row_by_id(MyModel, row_id: str):
    row = session.query(MyModel).filter(MyModel.id == row_id).first()
    if row:
        session.delete(row)
        session.commit()
        return {"message": "Row deleted successfully."}
    else:
        return {"message": "Row not found."} 
    
    

@app.get("/login",tags=["auth"])
async def github_login():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "scope": "user"
    }
    return {"url": f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"}

# Define the callback URL for Github OAuth2
@app.get("/auth/callback",tags=["auth"])
async def github_auth_callback(code: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url="https://github.com/login/oauth/access_token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": client_id,
                "client_secret": client_secret
            },
            headers={
                "Accept": "application/json"
            }
        )
        response.raise_for_status()
        access_token = response.json()["access_token"]
        return {"access_token": access_token, "token_type": "bearer"}

# Define an endpoint that requires Github authentication
@app.get("/me",tags=["user"])
async def read_current_user(token: str ):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url="https://api.github.com/user",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        user = response.json()
        return user

@app.get("/user/repos",tags=["Repositories"])
async def user_github_repository(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url=f"https://api.github.com/user/repos",
            headers={
                "Authorization": f"Bearer {token}"
            }
        )
        response.raise_for_status()
        repos = response.json()
        return repos

# boosted repository for all users.

@app.get("/boosted/repos",tags=["Boosted Repository"])
async def get_all_boosted_repository():
    repos = session.query(repoTable).filter(repoTable.status != 0).all()
    if repos:
        return [model_to_dict(rep) for rep in repos]
    else:
        return []
    

@app.post("/boosted/repos",tags=["Boosted Repository"])
async def create_boosted_repository(repo : Repo):
    repo = repoTable(username=repo.username,title=repo.title,status=repo.status,repolink=repo.repolink)
    session.add(repo)
    session.commit()
    return {"message":"reposity is boosted"}

@app.put("/boosted/repos/{id}",tags=["Boosted Repository"])
async def update_boosted_repository(id : int):
    res = session.query(repoTable).filter(repoTable.id == id).first()
    res.status = 0
    session.commit(res)
    return {"message":"repository status updated"}

@app.delete("/boosted/repos/{id}",tags=["Boosted Repository"])
async def delete_boosted_repository(id:int):
    res = delete_row_by_id(repoTable,id)
    return res
    
    
@app.get("/profile",tags=["Profile"])
async def user_profile(username : str):
    user = session.query(UserTable).filter(UserTable.username ==  username).first()
    if user:
        return model_to_dict(user)
    else:
        return []

@app.post("/profile/create",tags=["Profile"])
async def create_profile(username:str):
    user = UserTable(username=username,balance=0)
    session.add(user)
    session.commit()
    return {"message":"user profile has been created"}

