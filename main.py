#Python
from typing import List
import json
#Pydantic
#FastApi
from fastapi import FastAPI
from fastapi import status
from fastapi import Body
#TwitterApi
from models import Tweet,User,UserLogin,UserRegister

app=FastAPI()

#PathOperation

##Users
###Register a User
@app.post(
    path="/signup",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Register a User",
    tags=["Users"]
    )
def signup(user:UserRegister=Body(...)):
    """
    Signup

    this path operation register a user in the app

    Parameters:
    - Request Body Parameter
        - user:UserRegister
    
    Returns a Json with the basic user information:
        - user_id:UUID
        - email:EmailStr
        - first_name:str
        - last_name:str
        - birth_date:date
    """
    with open("users.json","r+",encoding="UTF-8") as f:
        results=json.loads(f.read())
        user_dict=user.dict()
        user_dict['user_id']=str(user_dict['user_id'])
        user_dict['birth_date']=str(user_dict['birth_date'])
        results.append(user_dict)
        f.seek(0)
        f.write(json.dumps(results))
        return user
###Login a user
@app.post(
    path="/login",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
    )
def login():
    pass
###Show all Users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all the users",
    tags=["Users"]
    )
def show_all_users():
    pass
###Show a User
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"]
    )
def show_a_user():
    pass
###Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_a_user():
    pass
###Update a User
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_a_user():
    pass

##Tweets
###Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all the tweets",
    tags=["Tweet"]
    )
def home():
    pass
###Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweet"]
    )
def post_a_tweet():
    pass

###Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweet"]
    )
def show_a_tweet():
    pass

###Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Delete a tweet",
    tags=["Tweet"]
    )
def delete_a_tweet():
    pass

###Update a tweet
@app.put(
    path="/tweets/{tweet_id}/update",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Update a tweet",
    tags=["Tweet"]
    )
def update_a_tweet():
    pass