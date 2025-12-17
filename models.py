from sqlalchemy import Column, Integer,String,Boolean,Text,ForeignKey
from database import Base
from sqlalchemy_utils import ChoiceType
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="user"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(25),unique=True)
    email=Column(String(80),unique=True)
    password=Column(Text,nullable=True)
    is_active=Column(Boolean,default=False)
    is_staff=Column(Boolean,default=False)

    orders=relationship("Order",back_populates="user")

    def __repr__(self):
        return f"<User{self.username}>"

class Order(Base):
    __tablename__="orders"
    ORDER_STATUSES=(
        ("PENDING","pending"),
        ("IN-TRANSIT","in-transit"),
        ("DELIVERED","delivered")
    )

    PIZZA_SIZES=(
        ("SMALL","small"),
        ("MEDIUM","medium"),
        ("LARGE","large")
    )

    id=Column(Integer,primary_key=True,index=True)
    quantity=Column(Integer,nullable=False)
    order_status=Column(ChoiceType(choices=ORDER_STATUSES),default="PENDING")
    pizza_size=Column(ChoiceType(choices=PIZZA_SIZES),default="SMALL")
    flavour=Column(String)
    user_id=Column(Integer,ForeignKey("user.id"))

    user=relationship("User",back_populates="orders")

    def __repr__(self):
        return f"<Order {self.id}>"