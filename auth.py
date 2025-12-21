from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal
from schemas import UserCreate,UserLogin
from models import User
from sqlalchemy.orm import Session
from utils import create_access_token
from passlib.context import CryptContext

router=APIRouter(prefix="/auth",tags=["auth"])

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup",response_model=UserCreate)
def signup(user:UserCreate,db: Session = Depends(get_db)):
    db_email=db.query(User).filter(User.email==user.email).first()

    if db_email is not None:
        raise HTTPException(status_code=400,detail="eamil alredy exists")
    
    db_username=db.query(User).filter(User.username==user.username).first()

    if db_username is not None:
        raise HTTPException(status_code=400,detail="username alredy exists")
     
    hashed=pwd_context.hash(user.password[:72])
    new_user=User(
        username=user.username,
        email=user.email,
        password=hashed,
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.post("/login")
def login(user:UserLogin,db:Session=Depends(get_db)):
    db_email=db.query(User).filter(User.email==user.email).first()

    if not db_email or not pwd_context.verify(user.password,str(db_email.password)):
        raise HTTPException(status_code=400,detail="enter valid password or email id")
    
    token=create_access_token({"user_id":db_email.id})
    
    return {
       "access_token":token,
       "token_type":"bearer",
       "user_id":db_email.id
    }
    

