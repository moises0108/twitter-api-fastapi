
from fastapi import HTTPException,status

from sqlalchemy.orm import Session



from . import models, schemas


def get_user(db: Session, user_id: int):
    have_user=db.query(models.User).get(user_id)
    if not have_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return have_user


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserRegister):
    db_user = models.User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        birth_date=user.birth_date,
        password=user.password
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session,user: schemas.UserLogin):
    take_user=db.query(models.User).filter(models.User.email==user.email).first()
    print(take_user)
    if not take_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if take_user.password!=user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return take_user

def get_tweet(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_user_tweet(db: Session, tweet: schemas.CreateTweet):
    exist_owner=db.query(models.User).filter(models.User.id==tweet.owner_id)

    if not db.query(exist_owner.exists()).scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db_item = models.Tweet(**tweet.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    tweet_create=tweet.dict()
    print((db.query(models.User).get(tweet.owner_id)).email)
    tweet_create["email"]=((db.query(models.User).get(tweet.owner_id)).email)    
    print(tweet_create)
    return tweet_create