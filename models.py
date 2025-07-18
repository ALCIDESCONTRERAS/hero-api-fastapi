from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

 
#define models users

class UserBase(SQLModel):
    username: str
    password: str
    
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    heroes: List["Hero"] = Relationship(back_populates="owner")

class CreateUser(UserBase):
    username: str
    password: str
 

# define models heroes
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: Optional[int] = Field(default=None, index=True)
    
class Hero(HeroBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    secret_name : str
    user_id: Optional[int] = Field(default=None, foreign_key="user.id", ondelete="CASCADE")
    owner : Optional[User] = Relationship(back_populates="heroes")
    
class HeroCreate(HeroBase):
    secret_name: str
    user_id: int
    
    model_config = {
        "from_attributes": True
    }
    
class HeroUpdate(HeroBase):
    name: Optional[str] = None
    age: Optional[int] = None
    secret_name : Optional[str] = None
    

class HeroRead(SQLModel):
    id: int
    name: str
    age: Optional[int] = None
    secret_name: str
    
class UserReadWithHeroes(SQLModel):
    id: int
    username: str
    heroes: List[HeroRead] = [] 