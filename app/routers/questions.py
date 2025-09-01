from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.database import get_session
from app import schemas
from app import DAO


router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=list[schemas.QuestionRead])
async def list_questions(session: AsyncSession = Depends(get_session)):
    return await DAO.list_questions(session)

@router.post("/", response_model=schemas.QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(payload: schemas.QuestionCreate, session: AsyncSession = Depends(get_session)):
    return await DAO.create_question(session, text=payload.text)

@router.get("/{question_id}", response_model=schemas.QuestionWithAnswers)
async def get_question(question_id: int, session: AsyncSession = Depends(get_session)):
    q = await DAO.get_question_with_answers(session, question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, session: AsyncSession = Depends(get_session)):
    ok = await DAO.delete_question(session, question_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Question not found")
