#Python
from typing import List
import json
#Pydantic
#FastApi
from fastapi import FastAPI
from fastapi import status,HTTPException
from fastapi import Body,Depends,Path
#TwitterApi

from twitt_app.database import SessionLocal,engine
from twitt_app.schemas import Tweet, UpdateUser,User,UserLogin,UserRegister,CreateTweet
from twitt_app import crud,models
#SqlAlchemy
from sqlalchemy.orm import Session
from sqlalchemy import event

app=FastAPI()
models.Base.metadata.create_all(bind=engine)
# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
event.listen(engine, 'connect', lambda c, _: c.execute('pragma foreign_keys=on'))
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
def signup(user:UserRegister=Body(...),db: Session = Depends(get_db)):
    """
    Signup

    this path operation register a user in the app

    Parameters:
    - Request Body Parameter
        - user:UserRegister
    
    Returns a Json with the basic user information:
    
        - email:EmailStr
        - first_name:str
        - last_name:str
        - birth_date:date
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
    
###Login a user
@app.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    tags=["Users"]
    )
def login(db: Session = Depends(get_db),user:UserLogin=Body(...)):
    """
    Login

    this path operation login a user in the app

    Parameters:
    - Request Body Parameter
        - user:UserLogin
    
    Returns a Json with the message 'login succesful'
    """
    return crud.login_user(db=db,user=user)
###Show all Users
@app.get(
    path="/users",
    response_model=List[User],
    status_code=status.HTTP_200_OK,
    summary="Show all the users",
    tags=["Users"]
    )
def show_all_users(db: Session = Depends(get_db)):
    """
    This path operation shows all user in the app

    Parameters:
        -None

    Returns a json list with all users in the app,with the following keys:
    
        - email:EmailStr
        - first_name:str
        - last_name:str
        - birth_date:date
    """
    return crud.get_users(db=db)
###Show a User
@app.get(
    path="/users/{user_id}",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Show a User",
    tags=["Users"],
    
    )
def show_a_user(
    user_id:int = Path(
        ...,
        gt=0,
        title="Person id",
        description="show a User with this id",
        example=1,
        ),
    db:Session=Depends(get_db)
    ):
    """
    Show a User

    this path operation show a user in the app

    Parameters:
    - Request Path Parameter
        - user_id
    
    Returns a Json with the basic user information:
    
        - email:EmailStr
        - first_name:str
        - last_name:str
        - birth_date:date
    """
    return crud.get_user(db=db,user_id=user_id)
###Delete a User
@app.delete(
    path="/users/{user_id}/delete",
    status_code=status.HTTP_200_OK,
    summary="Delete a User",
    tags=["Users"]
    )
def delete_a_user(
    user_id:int=Path(
        ...,
        gt=0,
        title="user id",
        description="id of the user you want delete",
        example=2
    ),
    db:Session=Depends(get_db)
):
   return crud.delete_user(db=db,user_id=user_id)
###Update a User
@app.put(
    path="/users/{user_id}/update",
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary="Update a User",
    tags=["Users"]
    )
def update_a_user(
    db:Session=Depends(get_db),
    user_id:int=Path(
        ...,
        gt=0,
        title="user_id",
        description="id of the user you want update"
        ),
    user:UpdateUser=Body(...)
    ):
    return crud.update_user(db,user_id,user)

##Tweets
###Show all tweets
@app.get(
    path="/",
    response_model=List[Tweet],
    status_code=status.HTTP_200_OK,
    summary="Show all the tweets",
    tags=["Tweet"]
    )
def home(db:Session = Depends(get_db)):
    """
    Home
    This path operation shows all tweets in the app

    Parameters:
        -None

    Returns a json list with all the tweets in the app,with the following keys:
    
        - tweet_id:UUID
        - by:User 
        - content:str
        - created_at:datetime 
        - updated_at:Optional[datetime]
    """
    return crud.get_tweet(db=db)
###Post a tweet
@app.post(
    path="/post",
    response_model=Tweet,
    status_code=status.HTTP_201_CREATED,
    summary="Post a tweet",
    tags=["Tweet"]
    )
def post_a_tweet(tweet: CreateTweet = Body(...),db:Session=Depends(get_db),):
    """
    Post a Tweet

    this path operation post a tweet in the app

    Parameters:
    - Request Body Parameter
        - tweet:CreateTweet
    
    Returns a Json with the basic tweet information:
    - email:EmailStr
    - content:str
    """
    return crud.create_user_tweet(db=db,tweet=tweet)

###Show a tweet
@app.get(
    path="/tweets/{tweet_id}",
    response_model=Tweet,
    status_code=status.HTTP_200_OK,
    summary="Show a tweet",
    tags=["Tweet"]
    )
def show_a_tweet(
    db:Session=Depends(get_db),
    tweet_id:int=Path(
        ...,gt=0,
        title="tweet_id",
        description="Id of the tweet that you want")
        ):
    """
    Show a Tweet

    this path operation show a tweet in the app

    Parameters:
    - Request Path Parameter
        - tweet_id
    
    Returns a Json with the basic tweet information:
    
        - content:str
        - userEmail:EmailStr
    """
    return crud.show_tweet(db,tweet_id)
###Delete a tweet
@app.delete(
    path="/tweets/{tweet_id}/delete",
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