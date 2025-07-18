from fastapi import APIRouter, HTTPException, Query
from sqlmodel import select
from typing import Annotated

from models import Hero, HeroCreate, HeroUpdate
from database import SessionDep

router_heroes = APIRouter(prefix="/heroes", tags=["Heroes"])

@router_heroes.post("/", response_model=Hero)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.from_orm(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero

@router_heroes.get("/", response_model=list[Hero])
def read_heroes(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes

@router_heroes.get("/{hero_id}", response_model=Hero)
def read_hero(hero_id:int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router_heroes.patch("/{hero_id}", response_model=Hero)
def update_hero(hero_id: int, hero:HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero no found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@router_heroes.delete("/{hero_id}")
def delete_hero(hero_id:int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}