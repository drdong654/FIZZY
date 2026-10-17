import asyncio

from sqlalchemy import select

from db.database import async_session_maker, engine
from db.models import Event, Mention, Persona, RawMessage, Source


async def get_or_create(session, model, **fields):
    obj = await session.scalar(select(model).filter_by(**fields))
    if obj is None:
        obj = model(**fields)
        session.add(obj)
        await session.flush()
    return obj


async def save_posts(posts):
    """Сохраняем посты с persona_key, персонами."""
    async with async_session_maker() as session:
        event = await get_or_create(session, Event, name="TechHeads 2026")
        source = await get_or_create(
            session, Source, kind="synthetic", title="Danish Personas"
        )

        for post in posts:
            exists = await session.scalar(
                select(RawMessage.id).where(
                    RawMessage.source_id == source.id,
                    RawMessage.external_id == str(post["persona_key"]),
                )
            )
            if exists is not None:
                continue

            persona = Persona(**post["persona"])
            session.add(persona)
            await session.flush()

            message = RawMessage(
                source_id=source.id,
                external_id=str(post["persona_key"]),
                text=post["text"],
            )
            session.add(message)
            await session.flush()

            session.add(
                Mention(
                    raw_message_id=message.id,
                    event_id=event.id,
                    persona_id=persona.id,
                    is_synthetic=True,
                )
            )

        await session.commit()


async def main():
    async with async_session_maker() as session:
        event = Event(name="DB check")
        source = Source(kind="test", title="DB check")
        session.add_all([event, source])
        await session.flush()

        message = RawMessage(source_id=source.id, text="DB check message")
        session.add(message)
        await session.flush()

        mention = Mention(raw_message_id=message.id, event_id=event.id)
        session.add(mention)
        await session.flush()

        statement = (
            select(Event.name, Source.kind, RawMessage.text)
            .select_from(Mention)
            .join(Event, Mention.event_id == Event.id)
            .join(RawMessage, Mention.raw_message_id == RawMessage.id)
            .join(Source, RawMessage.source_id == Source.id)
            .where(Mention.id == mention.id)
        )
        print((await session.execute(statement)).one())

        await session.rollback()  # Удаляет пробные записи этой транзакции.

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
