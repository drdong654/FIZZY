from typing import Optional
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

from sqlalchemy.orm import mapped_column
from sqlalchemy.dialects.postgresql import JSONB


class Base(DeclarativeBase):
    pass

class Persona(Base):
    
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True)
    persona_key: Mapped[str] = mapped_column(Text, unique=True, nullable=False)
    age: Mapped[Optional[int | None]] = mapped_column(nullable=True)
    gender: Mapped[str | None] = mapped_column(nullable=True)
    region: Mapped[str | None] = mapped_column(Text, nullable=True)
    occupation: Mapped[str | None] = mapped_column(Text, nullable=True)
    ocean: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)