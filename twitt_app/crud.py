
from cgi import print_form
from webbrowser import get
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
    if not take_user :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if take_user.password!=user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return {'msg':'Login succesfull!!'}

def delete_user(db:Session,user_id:int):
    db.query(models.User).filter(models.User.id==user_id).delete()
    db.commit()
    return {'msg':'User '+str(user_id)+' delete succesfull'}
    
def update_user(db:Session,user_id:int,user:schemas.UpdateUser):
    db_item=get_user(db,user_id)
    updated_user=user.dict(exclude_unset=True)

    for key,value in updated_user.items():
        if value!=None:
            print(value)
            setattr(db_item,key,value)

    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_tweet(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tweet).offset(skip).limit(limit).all()


def create_user_tweet(db: Session, tweet: schemas.CreateTweet):
    
    get_user(db=db,user_id=tweet.user_id)
    db_item = models.Tweet(**tweet.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    tweet_create=tweet.dict()
    tweet_create["email"]=((db.query(models.User).get(tweet.user_id)).email)    

    return tweet_create

def show_tweet(db:Session,tweet_id:int):
    get_tweet=db.query(models.Tweet).get(tweet_id)
    print(type(get_tweet))
    if not get_tweet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    get_user_email=db.query(models.User).get(get_tweet.user_id).email
    result={'content': get_tweet.content,'email': get_user_email}
    print(result)
    return  result
