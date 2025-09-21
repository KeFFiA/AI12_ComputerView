from sqlalchemy import select, func, delete, update
from sqlalchemy.ext.asyncio import AsyncSession


from Database import PDF_Queue


async def add_to_queue(session: AsyncSession, filename: str, user_email: str, _type: str):
    """
    Adds file to queue

    :param session: SQLAlchemy async session
    :param filename: file name
    :param user_email: user email
    :param _type: type of file(e.g. Claims)

    :return: PDF_Queue row object
    """
    result = await session.execute(select(func.max(PDF_Queue.queue_position)))
    max_pos = result.scalar()
    next_pos = 1 if max_pos is None else max_pos + 1

    row = PDF_Queue(
        filename=filename,
        user_email=user_email,
        type=_type,
        queue_position=next_pos
    )
    session.add(row)

    return row


async def remove_from_queue(session: AsyncSession) -> int:
    """
    Deletes all records whose status is NOT 'Queued' and NOT 'Processing',
    then rebuilds the queue positions.

    :param session: SQLAlchemy async session
    :return: number of records deleted
    """

    result = await session.execute(
        select(PDF_Queue.id, PDF_Queue.queue_position).where(
            PDF_Queue.status.notin_(["Queued", "Processing"])
        )
    )
    rows = result.all()
    if not rows:
        return 0

    await session.execute(
        delete(PDF_Queue).where(PDF_Queue.status.notin_(["Queued", "Processing"]))
    )

    ordered = await session.execute(
        select(PDF_Queue.id).order_by(PDF_Queue.queue_position.asc())
    )
    remaining_ids = [row[0] for row in ordered]

    for new_pos, row_id in enumerate(remaining_ids, start=1):
        await session.execute(
            update(PDF_Queue)
            .where(PDF_Queue.id == row_id)
            .values(queue_position=new_pos)
        )

    return len(rows)