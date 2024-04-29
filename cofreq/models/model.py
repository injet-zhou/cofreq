from __future__ import annotations

from typing import List

from pydantic import BaseModel


class Datum(BaseModel):
    id: str
    object: str
    created: int
    owned_by: str


class ModelsResponse(BaseModel):
    object: str
    data: List[Datum]
