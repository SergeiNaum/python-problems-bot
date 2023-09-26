from src.services.leaders import Leader, UserInLeaders
from src.services.questions import Question
from src.utils.formaters import format_explanation, format_leaders_message, format_question


def test_format_question() -> None:
    res = format_question(
        question=Question(
            id=1,
            text='text',
            answer='A',
            choices={'A': 1, 'B': 2},
            explanation='explanation'
        )
    )
    assert res == 'text\n\nA) 1\nB) 2'


def test_format_explanation() -> None:
    res = format_explanation(
        question=Question(
            id=1,
            text='text',
            answer='A',
            choices={'A': 1, 'B': 2},
            explanation='explanation'
        ),
        is_correct=True
    )
    assert res == 'text\n\n<b>Ответ:</b> A) 1\n\nПравильно ✅\n\n<b> Объяснение:</b>\nexplanation'


def test_format_leaders_message() -> None:
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=10),
        Leader(id=2, first_name='User2', username='user2', score=20),
        Leader(id=3, first_name='User3', username='user3', score=15),
    ]
    user_in_leaders = UserInLeaders(score=20, position=2)

    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=user_in_leaders)

    expected_message = (
        '<b>Таблица лидеров:</b>\n'
        '1. <a href="https://t.me/user1">User1</a> - 10 баллов\n'
        '2. <a href="https://t.me/user2">User2</a> - 20 баллов\n'
        '3. <a href="https://t.me/user3">User3</a> - 15 баллов\n'
        '\n'
        '<b>Ваше текущее место:</b> 2. Вы набрали 20 баллов.'
    )
    assert formatted_message == expected_message


def test_format_leaders_message__user_not_found() -> None:
    leaders = [
        Leader(id=1, first_name='User1', username='user1', score=10),
        Leader(id=2, first_name='User2', username='user2', score=20),
        Leader(id=3, first_name='User3', username='user3', score=15),
    ]

    formatted_message = format_leaders_message(leaders=leaders, user_in_leaders=None)

    expected_message = (
        '<b>Таблица лидеров:</b>\n'
        '1. <a href="https://t.me/user1">User1</a> - 10 баллов\n'
        '2. <a href="https://t.me/user2">User2</a> - 20 баллов\n'
        '3. <a href="https://t.me/user3">User3</a> - 15 баллов\n'
    )
    assert formatted_message == expected_message
