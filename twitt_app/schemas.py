#Python
from datetime import date
from typing import Optional
#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import ValidationError,validator
from sqlmodel import SQLModel
#Fast API
#twitterapi
from .database import Base


#Models
class UserBase(BaseModel):
    email:EmailStr = Field(
        ...,
        example="moisespatinoh@gmail.com"
    )
class User(UserBase):
    first_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Moises"
        )
    last_name:str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Patino"
        )
    
    birth_date : Optional[date] = Field(default=None,example="2000-08-01")
    
    class Config:
        orm_mode = True
    
    @validator('birth_date')
    def is_adult(cls,birth_date:date):
        today_date=date.today()
        if birth_date==None:
            return birth_date
        return over_18(birth_date,today_date)


def over_18(birth_date,today_date):
    diff_year=today_date.year-birth_date.year
    diff_month=today_date.month-birth_date.month
    diff_day=today_date.day<birth_date.day

    if diff_year<18 or (diff_year==18 and diff_month<0) :
        raise ValueError("Must be over 18")
    if(diff_year==18 and (diff_month==0) and diff_day):
        raise ValueError("Must be over 18")

    return birth_date

class UserLogin(UserBase):
    password:str = Field(
        ...,
        min_length=8,
        max_length=16,
        example="Moises123"
        )
class UserRegister(UserLogin,User):
    pass


class BaseTweet(BaseModel):
    content:str=Field(...,min_length=1,max_length=256)
class CreateTweet(BaseTweet):
    user_id:int = Field(...)
    
    class Config:
        orm_mode = True

class Tweet(BaseTweet,UserBase):
    pass

class UpdateUser(SQLModel):
    first_name:Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=50,
        example="Moises"
        )
    last_name:Optional[str]= Field(
        default=None,
        min_length=1,
        max_length=50,
        example="Patino"
        )
    email:Optional[EmailStr] = Field(
        default=None,
        example="moisespatinoh@gmail.com"
    )
    birth_date : Optional[date] = Field(default=None,example="2000-08-01")
    password:Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=16,
        example="Moises123"
        )
    @validator('birth_date')
    def is_adult(cls,birth_date:date):
        today_date=date.today()
        if birth_date==None:
            return None
        return over_18(birth_date,today_date)

class UpdateTweet(SQLModel):
    content:Optional[str]=Field(default=None,min_length=1,max_length=256)