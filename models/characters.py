from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class CharacterBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Character ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440011"},
    )
    name: str = Field(
        ...,
        description="Name of the character.",
        json_schema_extra={"example": "Naruto Uzumaki"},
    )
    role: str = Field(
        ...,
        description="Role of the character.",
        json_schema_extra={"example": "Protagonist"},
    )
    alias: Optional[str] = Field(
        None,
        description="Alias or Nickname of the character.",
        json_schema_extra={"example": "Seventh Hokage"},
    )
    gender: str = Field(
        None,
        description="Gender of the character.",
        json_schema_extra={"example": "Male"},
    )
    ability: str = Field(
        ...,
        description="Powers of the character.",
        json_schema_extra={"example": "Nine-Tails Chakra, Sage of six-paths"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440011",
                    "name": "Naruto Uzumaki",
                    "role": "Protagonist",
                    "alias": "Seventh Hokage",
                    "gender": "Male",
                    "ability": "Nine-Tails Chakra, Sage of six-paths",
                }
            ]
        }
    }


class CharacterCreate(CharacterBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111199",
                    "name": "Eren Yeager",
                    "role": "Protagonist",
                    "alias": "",
                    "gender": "Male",
                    "ability": "Attack Titan Power",
                }
            ]
        }
    }


class CharacterUpdate(BaseModel):
    """Partial update; character ID is taken from the path, not the body."""
    name: Optional[str] = Field(
        None,
        description="Name of the character.",
        json_schema_extra={"example": "Levi Ackerman"},
    )
    role: Optional[str] = Field(
        None,
        description="Role of the character.",
        json_schema_extra={"example": "Supporting"},
    )
    alias: Optional[str] = Field(
        None,
        description="Alias or Nickname of the character.",
        json_schema_extra={"example": "Humanity's Strongest Soldier"},
    )
    gender: str = Field(
        None,
        description="Gender of the character.",
        json_schema_extra={"example": "Male"},
    )
    ability: Optional[str] = Field(
        None,
        description="Powers of the character.",
        json_schema_extra={"example": "ODM mastery"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Levi Ackerman",
                    "role": "Supporting",
                    "alias": "Humanity's Strongest Soldier",
                    "gender": "Male",
                    "ability": "ODM mastery",
                },
                {"name": "Sasuke Uchiha",
                 "role": "Rival",
                },
            ]
        }
    }


class CharacterRead(CharacterBase):
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
                    "id": "550e8400-e29b-41d4-a716-446655440011",
                    "name": "Naruto Uzumaki",
                    "role": "Protagonist",
                    "alias": "Seventh Hokage",
                    "gender": "Male",
                    "ability": "Nine-Tails Chakra, Sage of six-paths",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                }
            ]
        }
    }
