import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.models import Question, Answer


@pytest.mark.asyncio
async def test_crud_flow(async_client: AsyncClient):
   # create question
        r = await async_client.post("/questions/", json={"text": "What is FastAPI?"})
        assert r.status_code == 201, r.text
        q = r.json()
        qid = q["id"]

        # list questions
        r = await async_client.get("/questions/")
        assert r.status_code == 200
        assert any(item["id"] == qid for item in r.json())

        # add answers (two from same user allowed)
        r = await async_client.post(f"/questions/{qid}/answers/", json={"user_id": "user-123", "text": "A modern web framework."})
        assert r.status_code == 201
        a1 = r.json()

        r = await async_client.post(f"/questions/{qid}/answers/", json={"user_id": "user-123", "text": "Built on Starlette & Pydantic."})
        assert r.status_code == 201
        a2 = r.json()

        # get single answer
        r = await async_client.get(f"/answers/{a1['id']}")
        assert r.status_code == 200
        assert r.json()["question_id"] == qid

        # get question with answers
        r = await async_client.get(f"/questions/{qid}")
        assert r.status_code == 200
        body = r.json()
        assert len(body["answers"]) == 2

        # delete one answer
        r = await async_client.delete(f"/answers/{a1['id']}")
        assert r.status_code == 204

        # still one answer left
        r = await async_client.get(f"/questions/{qid}")
        assert r.status_code == 200
        assert len(r.json()["answers"]) == 1

        # delete question -> cascade remove remaining answers
        r = await async_client.delete(f"/questions/{qid}")
        assert r.status_code == 204

        # question not found
        r = await async_client.get(f"/questions/{qid}")
        assert r.status_code == 404

        # answer not found
        r = await async_client.get(f"/answers/{a1['id']}")
        assert r.status_code == 404
        r = await async_client.get(f"/answers/{a2['id']}")
        assert r.status_code == 404
        
