import asyncio

from sqlalchemy import select

from db.database import async_session_maker, engine
from db.models import Event, Mention, RawMessage, Source


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