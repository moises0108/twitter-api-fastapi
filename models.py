#Python
from datetime import date,datetime
from uuid import UUID
from typing import Optional
#Pydantic
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from pydantic import ValidationError,validator
#Fast API



#Models
class UserBase(BaseModel):
    user_id:UUID = Field(...)
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
    
    @validator('birth_date')
    def is_adult(cls,birth_date):
        today_date=date.today()
        total_years=today_date-birth_date

        if total_years.years<18:
            raise ValueError("Must be over 18")
        else:
            return birth_date
class UserLogin(UserBase):
    password:str = Field(
        ...,
        min_length=8,
        max_length=16,
        example="Moises123"
        )

class Tweet(BaseModel):
    id:UUID=Field(...)
    by:User = Field(...)
    content:str=Field(...,min_length=1,max_length=256)
    created_at:datetime = Field(default=datetime.now())
    update_now:Optional[datetime] = Field(default=None) 
