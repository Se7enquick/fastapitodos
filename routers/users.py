import sys
sys.path.append('..')

from .auth import get_current_user, verify_password, get_password_hash
from fastapi import Depends, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from helpers import http_exception, get_user_exception
from pydantic import BaseModel

router = APIRouter(prefix='/users', tags=['users'], responses={404: {'description': 'User not found'}})

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str


@router.get('/')
async def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@router.get('/{user_id}')
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(
        models.Users.id == user_id).first()
    if user is not None:
        return user
    raise http_exception(404, 'User not found')


@router.put('user/password')
async def user_password_change(user_verification: UserVerification, user: dict = Depends(get_current_user),
                               db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(user_verification.password,
                                                                                 user_model.hashed_password):
            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return 'Success'
        return 'Invalid user or request'


@router.delete('/user')
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise get_user_exception()

    user_model = db.query(models.Users).filter(models.Users.id == user.get('id')).first()

    if user_model is None:
        return "Invalid user of request"

    db.query(models.Users).filter(models.Users.id == user.get('id')).delete()
    db.commit()
    return 'User was deleted'
