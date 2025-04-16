from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.services import handle_start, handle_join, handle_chrono

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    await handle_start(message)


@router.message(Command("join"))
async def cmd_join(message: types.Message):
    await handle_join(message)


@router.message(Command("chrono"))
async def cmd_join(message: types.Message):
    await handle_chrono(message)
