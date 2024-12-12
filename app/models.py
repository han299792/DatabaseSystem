from pydantic import BaseModel

class Review(BaseModel):
    author: str
    review: str
