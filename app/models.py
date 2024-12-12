from pydantic import BaseModel, Field
from typing import List

class Review(BaseModel):
    author: str
    review: str

class Address(BaseModel):
    si: str
    gu: str
    dong: str
    detail: str
    distance: dict 

class Restaurant(BaseModel):
    res_id: str
    name: str
    address: Address
    phone: str

class Customer(BaseModel):
    cus_id: str
    cus_name: str
    address: Address

