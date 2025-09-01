from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app import schemas
from app import DAO

router = APIRouter(prefix="", tags=["answers"])

@router.post("/questions/{question_id}/answers/", response_model=schemas.AnswerRead, status_code=status.HTTP_201_CREATED)
async def add_answer(question_id: int, payload: schemas.AnswerCreate, session: AsyncSession = Depends(get_session)):
    a = await DAO.create_answer(session, payload, question_id)
    if not a:
        raise HTTPException(status_code=404, detail="Question not found")
    return a

@router.get("/answers/{answer_id}", response_model=schemas.AnswerRead)
async def get_answer(answer_id: int, session: AsyncSession = Depends(get_session)):
    a = await DAO.get_answer(session, answer_id)
    if not a:
        raise HTTPException(status_code=404, detail="Answer not found")
    return a

@router.delete("/answers/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, session: AsyncSession = Depends(get_session)):
    ok = await DAO.delete_answer(session, answer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Answer not found")
