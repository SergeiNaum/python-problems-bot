import json
import random

import asyncpg
from pydantic import BaseModel

from settings import bot_settings
from src.repositories.postgres.questions import QuestionsRepo
from src.utils.is_answer_correct import is_answer_correct


class Question(BaseModel):
    id: int  # noqa A003
    text: str
    answer: str
    choices: dict
    explanation: str | None


class QuestionsService:
    def __init__(self, pg_pool: asyncpg.Pool) -> None:
        self.repo = QuestionsRepo(pg_pool=pg_pool)

    async def get_new_random_question_for_user(
            self, user_id: int, user_level: int
    ) -> Question | None:
        today_answered_questions_count = await self.repo.get_today_answered_questions_count(
            user_id=user_id
        )
        if today_answered_questions_count >= bot_settings.MAX_QUESTION_PER_DAY:
            return

        rows = await self.repo.get_new_questions_for_user(
            user_id=user_id,
            level=user_level,
            limit=10
        )
        if not rows:
            return

        row = random.choice(rows)
        return Question(
            id=row['id'],
            text=row['text'],
            answer=row['answer'],
            explanation=row['explanation'],
            choices=json.loads(row['choices']),
        )

    async def _get_by_id(self, question_id: int) -> Question | None:
        row = await self.repo.get_by_id(question_id=question_id)
        if not row:
            return
        return Question(
            id=row['id'],
            text=row['text'],
            answer=row['answer'],
            explanation=row['explanation'],
            choices=json.loads(row['choices']),
        )

    async def answer_question(
        self,
        user_id: int,
        question_id: int,
        user_answer: str
    ) -> tuple[Question | None, bool | None]:
        question: Question = await self._get_by_id(question_id=question_id)
        if not question:
            return None, None

        is_correct = is_answer_correct(user_answer=user_answer, correct_answer=question.answer)
        await self.repo.answer_question(
            question_id=question.id,
            user_id=user_id,
            user_answer=user_answer,
            is_correct=is_correct,
        )

        return question, is_correct