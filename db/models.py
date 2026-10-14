from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    false,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):

    pass

class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
        )
    name: Mapped[str] = mapped_column(
        Text, 
        nullable=False
        )
    starts_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
        )

class Keyword(Base):
    __tablename__ = "keywords"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    event_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("events.id"),
        nullable=False,
    )
    term: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

class Source(Base):
    __tablename__ = "sources"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
        )
    kind: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    handle: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )


class Persona(Base):
    __tablename__ = "personas"
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
        )
    age: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )
    gender: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    region: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    occupation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    ocean: Mapped[dict[str, object] | None] = mapped_column(
        JSONB,
        nullable=True
    )
    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

class RawMessage(Base):
    __tablename__ = "raw_messages"
    __table_args__ = (
    UniqueConstraint("source_id", "external_id"),
    )
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True
        )
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("sources.id"),
        nullable=False,
    )
    external_id: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    author: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    posted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    fetched_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        server_default=func.now(),
    )

class Mention(Base):
    __tablename__ = "mentions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )
    raw_message_id: Mapped[int] = mapped_column(
        ForeignKey("raw_messages.id"),
        nullable=False,
    )
    event_id: Mapped[int] = mapped_column(
        ForeignKey("events.id"),
        nullable=False,
    )
    persona_id: Mapped[int | None] = mapped_column(
        ForeignKey("personas.id"),
        nullable=True,
    )
    sentiment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    topics: Mapped[list[str] | None] = mapped_column(
        ARRAY(Text),
        nullable=True,
    )
    is_synthetic: Mapped[bool | None] = mapped_column(
        Boolean,
        nullable=True,
        server_default=false(),
    )