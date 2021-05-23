#
# models.py
#
from pydantic import BaseModel
from datetime import  date, time, datetime


class User(BaseModel):
    userId: int
    userName: str
    userEmail: str 

class FullUser(User):
    dateCreated: datetime

class SaylorPost(BaseModel):
    saylorId: int
    reference: str
    court: str
    nameFirst: str
    nameLast: str
    testator: str
    shipName: str
    dateOfWill: date
    dateOfProbate: date
    role: str
    married: bool
    notes: str

class Saylor(SaylorPost):
    creationDate: datetime
    lastModified: datetime
    createdBy: str

