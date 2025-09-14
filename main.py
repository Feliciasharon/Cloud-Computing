from __future__ import annotations

import os
import socket
from datetime import datetime

from typing import Dict, List
from uuid import UUID

from fastapi import FastAPI, HTTPException
from fastapi import Query, Path
from typing import Optional

from models.anime import AnimeCreate, AnimeRead, AnimeUpdate
from models.characters import CharacterCreate, CharacterRead, CharacterUpdate
from models.health import Health

port = int(os.environ.get("FASTAPIPORT", 8003))

# -----------------------------------------------------------------------------
# Fake in-memory "databases"
# -----------------------------------------------------------------------------

animes: Dict[UUID, AnimeRead] = {}
characters: Dict[UUID, CharacterRead] = {}

app = FastAPI(
    title="Anime/Character API",
    description="Demo FastAPI app using Pydantic v2 models for Anime and Characters",
    version="0.1.0",
)


def make_health(echo: Optional[str], path_echo: Optional[str]=None) -> Health:
    return Health(
        status=200,
        status_message="OK",
        timestamp=datetime.utcnow().isoformat() + "Z",
        ip_address=socket.gethostbyname(socket.gethostname()),
        echo=echo,
        path_echo=path_echo
    )

@app.get("/health", response_model=Health)
def get_health_no_path(echo: str | None = Query(None, description="Optional echo string")):
    # Works because path_echo is optional in the model
    return make_health(echo=echo, path_echo=None)

@app.get("/health/{path_echo}", response_model=Health)
def get_health_with_path(
    path_echo: str = Path(..., description="Required echo in the URL path"),
    echo: str | None = Query(None, description="Optional echo string"),
):
    return make_health(echo=echo, path_echo=path_echo)


# -----------------------------------------------------------------------------
# Character endpoints
# -----------------------------------------------------------------------------
@app.post("/characters", response_model=CharacterRead, status_code=201)
def create_character(character: CharacterCreate):
    if character.id in characters:
        raise HTTPException(status_code=400, detail="Character with this ID already exists")
    characters[character.id] = CharacterRead(**character.model_dump())
    return characters[character.id]

@app.get("/characters", response_model=List[CharacterRead])
def list_characters(
    name: Optional[str] = Query(None, description="Filter by name"),
    role: Optional[str] = Query(None, description="Filter by role"),
    alias: Optional[str] = Query(None, description="Filter by alias"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
    ability: Optional[str] = Query(None, description="Filter by ability"),
):
    results = list(characters.values())

    if name is not None:
        results = [a for a in results if a.name == name]
    if role is not None:
        results = [a for a in results if a.role == role]
    if alias is not None:
        results = [a for a in results if a.alias == alias]
    if gender is not None:
        results = [a for a in results if a.gender == gender]
    if ability is not None:
        results = [a for a in results if a.ability == ability]

    return results

@app.get("/characters/{character_id}", response_model=CharacterRead)
def get_character(character_id: UUID):
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="character not found")
    return characters[character_id]

@app.patch("/characters/{character_id}", response_model=CharacterRead)
def update_character(character_id: UUID, update: CharacterUpdate):
    if character_id not in characters:
        raise HTTPException(status_code=404, detail="Character not found")
    stored = characters[character_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    characters[character_id] = CharacterRead(**stored)
    return characters[character_id]


# -----------------------------------------------------------------------------
# Anime endpoints
# -----------------------------------------------------------------------------
@app.post("/animes", response_model=AnimeRead, status_code=201)
def create_anime(anime: AnimeCreate):
    # Each anime gets its own UUID; stored as AnimeRead
    anime_read = AnimeRead(**anime.model_dump())
    animes[anime_read.id] = anime_read
    return anime_read

@app.get("/animes", response_model=List[AnimeRead])
def list_animes(
    title: Optional[str] = Query(None, description="Filter by title"),
    genre: Optional[str] = Query(None, description="Filter by genre"),
    seasons: Optional[str] = Query(None, description="Filter by seasons"),
    rating: Optional[str] = Query(None, description="Filter by rating"),
    status: Optional[str] = Query(None, description="Filter by status"),
    streaming: Optional[str] = Query(None, description="Filter by streaming"),
    role: Optional[str] = Query(None, description="Filter by role"),
    gender: Optional[str] = Query(None, description="Filter by gender"),
):
    results = list(animes.values())

    if title is not None:
        results = [p for p in results if p.title == title]
    if genre is not None:
        results = [p for p in results if p.genre == genre]
    if seasons is not None:
        results = [p for p in results if p.seasons == seasons]
    if rating is not None:
        results = [p for p in results if p.rating == rating]
    if status is not None:
        results = [p for p in results if p.status == status]
    if streaming is not None:
        results = [p for p in results if str(p.streaming) == streaming]

    # nested character filtering
    if role is not None:
        results = [p for p in results if any(char.role == role for char in p.characters)]
    if gender is not None:
        results = [p for p in results if any(char.gender == gender for char in p.addresses)]

    return results

@app.get("/animes/{anime_id}", response_model=AnimeRead)
def get_anime(anime_id: UUID):
    if anime_id not in animes:
        raise HTTPException(status_code=404, detail="Anime not found")
    return animes[anime_id]

@app.patch("/animes/{anime_id}", response_model=AnimeRead)
def update_anime(anime_id: UUID, update: AnimeUpdate):
    if anime_id not in animes:
        raise HTTPException(status_code=404, detail="Anime not found")
    stored = animes[anime_id].model_dump()
    stored.update(update.model_dump(exclude_unset=True))
    animes[anime_id] = AnimeRead(**stored)
    return animes[anime_id]


# -----------------------------------------------------------------------------
# Root
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {"message": "Welcome to the Anime/Character API. See /docs for OpenAPI UI."}

# -----------------------------------------------------------------------------
# Entrypoint for `python main.py`
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
