import sys
sys.path.append('..')

from typing import Optional
from fastapi import Depends, APIRouter
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .auth import get_current_user
from helpers import get_user_exception


router = APIRouter(prefix='/address', tags=['address'], responses={404: {'description': 'Not found'}})


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Address(BaseModel):
    address: str
    city: str
    country: str
    postalcode: str


@router.post('/')
async def create_address(address: Address, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()

    address_model = models.Address()
    address_model.address = address.address
    address_model.city = address.city
    address_model.country = address.country
    address_model.postalcode = address.postalcode

    db.add(address_model)
    db.flush()




