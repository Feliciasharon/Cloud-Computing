from __future__ import annotations

from typing import Optional, List, Annotated
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field
from .characters import CharacterBase

class AnimeBase(BaseModel):
    title: str = Field(
        ...,
        description="Name of the anime.",
        json_schema_extra={"example": "Naruto"},
    )
    genre: str = Field(
        ...,
        description="Genre of the anime.",
        json_schema_extra={"example": "Comedy/Action"},
    )
    seasons: str = Field(
        ...,
        description="Number of seasons the anime was playing.",
        json_schema_extra={"example": "9"},
    )
    rating: Optional[str] = Field(
        None,
        description="Rating of the anime.",
        json_schema_extra={"example": "5"},
    )
    status: str = Field(
        ...,
        description="Status of the anime.",
        json_schema_extra={"example": "Ongoing"},
    )
    streaming: str = Field(
        ...,
        description="Platforms of the anime.",
        json_schema_extra={"example": "Netflix/Crunchyroll"},
    )

    # Embed characters (each with persistent ID)
    characters: List[CharacterBase] = Field(
        default_factory=list,
        description="Characters linked to this Anime (each carries a persistent Character ID).",
        json_schema_extra={
            "example": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Naruto Uzumaki",
                    "role": "Protagonist",
                    "alias": "Seventh Hokage",
                    "gender": "Male",
                    "ability": "Nine-Tails Chakra, Sage of six-paths",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Naruto",
                    "genre": "Comedy/Action",
                    "seasons": "9",
                    "rating": "5",
                    "status": "Ongoing",
                    "streaming": "Netflix/Crunchyroll",
                    "characters": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Naruto Uzumaki",
                            "role": "Protagonist",
                            "alias": "Seventh Hokage",
                            "gender": "Male",
                            "ability": "Nine-Tails Chakra, Sage of six-paths",
                        }
                    ],
                }
            ]
        }
    }


class AnimeCreate(AnimeBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Attack on Titan",
                    "genre": "Action",
                    "seasons": "4",
                    "rating": "5",
                    "status": "Completed",
                    "streaming": "Crunchyroll",
                    "characters": [
                        {
                            "id": "11111111-1111-4111-8111-111111111111",
                            "name": "Eren Yeager",
                            "role": "Protagonist",
                            "alias": "",
                            "gender": "Male",
                            "ability": "Attack Titan Power",
                        }
                    ],
                }
            ]
        }
    }


class AnimeUpdate(BaseModel):
    """Partial update."""
    title: Optional[str] = Field(
        None,
        description="Name of the anime.",
        json_schema_extra={"example": "Naruto"},
    )
    genre: Optional[str] = Field(
        None,
        description="Genre of the anime.",
        json_schema_extra={"example": "Comedy/Action"},
    )
    seasons: Optional[str] = Field(
        None,
        description="Number of seasons the anime was playing.",
        json_schema_extra={"example": "9"},
    )
    rating: Optional[str] = Field(
        None,
        description="Rating of the anime.",
        json_schema_extra={"example": "5"},
    )
    status: Optional[str] = Field(
        None,
        description="Status of the anime.",
        json_schema_extra={"example": "Ongoing"},
    )
    streaming: Optional[str] = Field(
        None,
        description="Platforms of the anime.",
        json_schema_extra={"example": "Netflix/Crunchyroll"},
    )
    characters: Optional[List[CharacterBase]] = Field(
        None,
        description="Replace the entire set of characters with this list.",
        json_schema_extra={
            "example": [
                {
                    "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb",
                    "name": "Sasuke Uchiha",
                    "role": "Rival",
                    "alias": "",
                    "gender": "Male",
                    "ability": "Sharingan, Chidori",
                }
            ]
        },
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "characters": [
                        {
                            "id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbttt77",
                            "name": "Levi Ackerman",
                            "role": "Supporting",
                            "alias": "Humanity's Strongest Soldier",
                            "gender": "Male",
                            "ability": "ODM mastery",
                        }
                    ]
                },
                {
                    "title": "Solo Leveling",
                    "genre": "Action",
                    "seasons": "2",
                    "rating": "4",
                    "status": "Ongoing",
                    "streaming": "Crunchyroll",
                },
                {"status": "Ongoing"},
            ]
        }
    }


class AnimeRead(AnimeBase):
    """Server representation returned to clients."""
    id: UUID = Field(
        default_factory=uuid4,
        description="Server-generated Person ID.",
        json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"},
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "title": "Naruto",
                    "genre": "Comedy/Action",
                    "seasons": "9",
                    "rating": "5",
                    "status": "Ongoing",
                    "streaming": "Netflix/Crunchyroll",
                    "characters": [
                        {
                            "id": "550e8400-e29b-41d4-a716-446655440000",
                            "name": "Naruto Uzumaki",
                            "role": "Protagonist",
                            "alias": "Seventh Hokage",
                            "gender": "Male",
                            "ability": "Nine-Tails Chakra, Sage of six-paths",
                        }
                    ],
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
