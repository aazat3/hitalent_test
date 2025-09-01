from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


from app import models, schemas


# ---- Questions ----
async def list_questions(session: AsyncSession) -> list[models.Question]:
    res = await session.execute(select(models.Question).order_by(models.Question.id))
    return list(res.scalars())

async def create_question(session: AsyncSession, text: str) -> models.Question:
    q = models.Question(text=text)
    session.add(q)
    await session.commit()
    await session.refresh(q)
    return q

async def get_question_with_answers(session: AsyncSession, question_id: int) -> models.Question | None:
    res = await session.execute(
        select(models.Question).where(models.Question.id == question_id)
    )
    q = res.scalars().first()
    if q:
        # lazy-load answers (relationship is lazy='select' by default)
        await session.refresh(q, attribute_names=["answers"])
    return q

async def delete_question(session: AsyncSession, question_id: int) -> bool:
    res = await session.execute(select(models.Question).where(models.Question.id == question_id))
    q = res.scalar_one_or_none()
    if not q:
        return False
    await session.delete(q)  # CASCADE на FK удалит ответы
    await session.commit()
    return True

# ---- Answers ----
async def create_answer(
    session: AsyncSession, payload: schemas.AnswerCreate, question_id:int,
) -> models.Answer | None:
    q = await session.get(models.Question, question_id)
    if not q:
        return None
    a = models.Answer(question_id=question_id, user_id=payload.user_id, text=payload.text)
    session.add(a)
    await session.commit()
    await session.refresh(a)
    return a

async def get_answer(session: AsyncSession, answer_id: int) -> models.Answer | None:
    return await session.get(models.Answer, answer_id)

async def delete_answer(session: AsyncSession, answer_id: int) -> bool:
    res = await session.execute(select(models.Answer).where(models.Answer.id == answer_id))
    a = res.scalar_one_or_none()
    if not a:
        return False
    await session.delete(a)
    await session.commit()
    return True