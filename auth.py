from fastapi import APIRouter,HTTPException,Depends
from database import SessionLocal
from schemas import UserCreate,UserLogin
from models import User
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy.orm import Session
router=APIRouter(prefix="/auth",tags=["auth"])


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
    
    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

