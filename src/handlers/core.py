from aiogram import Router, types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy import select

from db.engine import async_session_maker
from db.models import ToDo

router = Router()


class ToDoStatesGroup(StatesGroup):
    create = State()
    set_active_is_false = State()


@router.message(State('*'), Command('cancel'))
async def cancel_handler(
    message: types.Message,
    state: FSMContext,
):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.reply('Создание отменено')


@router.message(Command('todo'))
async def get_todo_list(
    message: types.Message,
    bot: Bot,
) -> None:
    async with async_session_maker() as session:
        todos = (
            (
                await session.execute(
                    select(ToDo).where(ToDo.is_active.is_(True)).limit(100)
                )
            )
            .scalars()
            .all()
        )
    if not todos:
        text = 'У вас нет ToDo'
    else:
        text = 'Ваши ToDo:\n\n'
        for todo in todos:
            text += (
                f'<code>ID: {todo.id}\n'
                f'Заголовок: {todo.title}\n'
                f'Описание: {todo.description}\n'
                f'Приоритет: {todo.priority.value}\n</code>\n'
            )
    await bot.send_message(
        message.from_user.id,
        text,
        parse_mode='html',
    )


@router.message(Command('create_todo'))
async def create_todo_start(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(ToDoStatesGroup.create)
    await bot.send_message(
        message.from_user.id,
        'Для создания `ToDo` пришлите сообщение в следующем формате:\n\n'
        '<code>Заголовок\nОписание\nПриоритет (низкий/средний/высокий)</code>',
        parse_mode='html',
    )


@router.message(ToDoStatesGroup.create)
async def create_todo(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    priorities = {'низкий': 'low', 'средний': 'medium', 'высокий': 'high'}
    title, description, priority = message.text.split('\n')
    async with async_session_maker() as session:
        session.add(
            ToDo(
                title=title,
                description=description,
                priority=priorities.get(priority) or 'low',
            )
        )
        await session.commit()
    await state.clear()
    await bot.send_message(message.from_user.id, 'ToDo создана!')


@router.message(Command('set_done'))
async def set_active_false_start(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    await state.set_state(ToDoStatesGroup.set_active_is_false)
    await bot.send_message(
        message.from_user.id,
        'Отправьте id ToDo',
        parse_mode='html',
    )


@router.message(ToDoStatesGroup.set_active_is_false)
async def set_active_false(
    message: types.Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    async with async_session_maker() as session:
        todo = await session.get(ToDo, 1)
        todo.is_active = False
        await session.commit()
    await state.clear()
    await bot.send_message(message.from_user.id, 'ToDo отмечена сделанной!')
