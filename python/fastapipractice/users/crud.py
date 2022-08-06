from sqlalchemy.orm import Session

from . import models, schemas
import datetime

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(sns_id=user.sns_id, email=user.email, name=user.name,
                          access_token=user.access_token, refresh_token=user.refresh_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, db_user: models.User):
    # updates = schemas.User(id=db_user.id, sns_id=db_user.sns_id, is_active=True)
    # update_data = updates.dict(exclude_unset=True)
    # for key, value in update_data.items():
    #     setattr(db_user, key, value)
    setattr(db_user, 'last_login_at', datetime.datetime.now())
    db.commit()
    return db_user
