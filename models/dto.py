from dataclasses import dataclass
from typing import Optional


@dataclass
class ParsedQuery:

    intent: str

    campus: str | None

    cafeteria_seq: str | None

    meal_type: str | None

    ymd: str | None

    original_text: str


@dataclass
class MenuItem:

    course: str

    main: str

    sides: list[str]

    kcal: str

    rating: float

    rating_count: int

    origin: str

    soldout: bool

    congestion: str

    guide: str


@dataclass
class ChatResponse:

    success: bool

    message: str

    data: dict