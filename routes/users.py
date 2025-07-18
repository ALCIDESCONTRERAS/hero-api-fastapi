from fastapi import APIRouter, HTTPException
from sqlmodel import select
from sqlalchemy.orm import selectinload

from models import CreateUser, User, UserReadWithHeroes
from database import SessionDep

router_user = APIRouter(prefix="/users", tags=["Users"])

@router_user.post("/", response_model=User)
def create_user(user: CreateUser, session: SessionDep):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
    
@router_user.get("/", response_model= list[User])
def get_users(session: SessionDep):
    return session.exec(select(User)).all()

@router_user.get("/{user_id}", response_model=UserReadWithHeroes)
def get_user(user_id: int, session: SessionDep):
    statement = select(User).where(User.id == user_id).options(selectinload(User.heroes))
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router_user.delete("/{user_id}")
def delete_user(user_id: int, session: SessionDep):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"message": "User deleted"}
