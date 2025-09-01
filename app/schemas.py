from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ---- QUESTIONS ----
class QuestionCreate(BaseModel):
    text: str = Field(min_length=1, max_length=10_000)

class QuestionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    text: str
    created_at: datetime

class QuestionWithAnswers(QuestionRead):
    answers: list["AnswerRead"] = []

# ---- ANSWERS ----
class AnswerCreate(BaseModel):
    user_id: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=1, max_length=10_000)


class AnswerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    question_id: int
    user_id: str
    text: str
    created_at: datetime