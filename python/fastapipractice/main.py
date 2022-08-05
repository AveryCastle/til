from typing import Optional

import httpx
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()


@app.get("/")
async def read_root():
    return {"Hello": "World"}


# naver login
@app.get("/api/v1/naver/login")
def login_naver():
    client_id = "OhxX7JadJJxQ82m7g4aU"
    redirect_uri = "http://localhost:8000/api/v1/member/naver/auth"
    url = f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&state=STATE_STRING&redirect_uri={redirect_uri}"
    return RedirectResponse(url)


# naver auth
@app.get("/api/v1/member/naver/auth")
def login_callback(code: Optional[str] = None, state: Optional[str] = None,
                   error: Optional[str] = None, error_description: Optional[str] = None):
    client_id = "OhxX7JadJJxQ82m7g4aU"
    client_secret = "zWD718J4fm"

    token_request_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
    response = httpx.get(token_request_url)
    response_data = response.json()

    access_token = response_data.get("access_token")
    response = httpx.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_data = response.json()

    return profile_data
