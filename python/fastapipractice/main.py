from typing import Optional

import httpx
from fastapi import FastAPI, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from users import models, schemas, crud
from users.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
                   error: Optional[str] = None, error_description: Optional[str] = None, db: Session = Depends(get_db)):
    client_id = "OhxX7JadJJxQ82m7g4aU"
    client_secret = "zWD718J4fm"

    token_request_url = f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&state={state}"
    response = httpx.get(token_request_url)
    response_data = response.json()

    access_token = response_data.get("access_token")
    response = httpx.get("https://openapi.naver.com/v1/nid/me", headers={"Authorization": f"Bearer {access_token}"})
    profile_response = response.json()
    print(" profile_date = %r" % profile_response)
    print(" profile_data.response = %r" % profile_response.get('response'))

    profile_data = profile_response.get('response')
    user_date = schemas.UserCreate(sns_id=profile_data.get('id'),
                                   email=profile_data.get('email'),
                                   name=profile_data.get('name'),
                                   access_token=response_data.get('access_token'),
                                   refresh_token=response_data.get('refresh_token'))

    db_user = crud.get_user_by_email(db, email=user_date.email)
    if db_user:
        print("db_user = %r" % db_user)
        updated_user = crud.update_user(db=db, db_user=db_user)
        return schemas.User(id=updated_user.id, sns_id=updated_user.sns_id, is_active=True)
    else:
        saved_user = crud.create_user(db=db, user=user_date)
        return schemas.User(id = saved_user.id, sns_id = saved_user.sns_id, is_active = True)
