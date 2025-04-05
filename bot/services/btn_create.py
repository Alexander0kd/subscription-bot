from datetime import datetime, date, timedelta

from aiogram.types import CallbackQuery

from bot.keyboards import get_cancel_keyboard, get_period_create_keyboard, get_confirm_keyboard, \
    get_order_create_keyboard, get_main_keyboard
from config.settings import DAYS_IN_SUBSCRIPTION_MONTH
from db.crud.group_crud import create_group_with_custom_join_id
from db.models import PaymentPeriod, PaymentMethod, GroupModel
from db.utils import generate_join_id, get_displayed_date
from translation import localize_text
from aiogram import types, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


router = Router()


class CreateGroupStates(StatesGroup):
    GET_NAME = State()
    GET_AMOUNT = State()
    GET_PAYMENT_DATE = State()
    GET_PERIOD = State()
    GET_PERIOD_ORDER = State()
    GET_COMMENT = State()
    CONFIRM = State()


async def create_group(message: types.Message, state: FSMContext):
    """Початок створення групи"""
    await message.answer(
        text=localize_text('messages.create_name'),
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(CreateGroupStates.GET_NAME)


@router.message(CreateGroupStates.GET_NAME)
async def process_group_name(message: types.Message, state: FSMContext):
    """Обробка назви групи"""
    if len(message.text) > 50:
        await message.answer(localize_text('errors.too_long', len=50))
        return

    await state.update_data(name=message.text)

    await message.answer(
        text=localize_text('messages.create_sum'),
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(CreateGroupStates.GET_AMOUNT)


@router.message(CreateGroupStates.GET_AMOUNT)
async def process_group_amount(message: types.Message, state: FSMContext):
    """Обробка суми оплати"""
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer(localize_text('errors.nan'))
            return

        await state.update_data(amount=amount)
        await message.answer(
            text=localize_text('messages.create_period'),
            reply_markup=get_period_create_keyboard()
        )
        await state.set_state(CreateGroupStates.GET_PERIOD)
    except ValueError:
        await message.answer(localize_text('errors.nan'))


@router.callback_query(CreateGroupStates.GET_PERIOD, F.data.in_([PaymentPeriod.DAILY, PaymentPeriod.WEEKLY, PaymentPeriod.MONTHLY]))
async def process_payment_period(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору періоду оплати з кнопок"""
    await state.update_data(period=callback.data)
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        text=localize_text('messages.create_order'),
        reply_markup=get_order_create_keyboard()
    )
    await state.set_state(CreateGroupStates.GET_PERIOD_ORDER)


@router.callback_query(CreateGroupStates.GET_PERIOD_ORDER, F.data.in_([PaymentMethod.EACH_USER, PaymentMethod.TURN_RANDOM, PaymentMethod.TURN_JOIN_DATE]))
async def process_payment_order(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору періоду оплати з кнопок"""
    await state.update_data(period_order=callback.data)
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        text=localize_text('messages.create_date'),
        reply_markup=get_cancel_keyboard()
    )
    await state.set_state(CreateGroupStates.GET_PAYMENT_DATE)


@router.message(CreateGroupStates.GET_PAYMENT_DATE)
async def process_payment_date(message: types.Message, state: FSMContext):
    """Обробка дати оплати"""
    try:
        user_date = datetime.strptime(message.text, "%d.%m")
        next_payment_date = user_date.replace(year=date.today().year)

        if next_payment_date.date() < date.today():
            data = await state.get_data()
            period = PaymentPeriod[data.get("period", "MONTHLY").upper()]
            now = datetime.now()

            if period == PaymentPeriod.DAILY:
                next_payment_date = now + timedelta(days=1)
            elif period == PaymentPeriod.WEEKLY:
                next_payment_date = now + timedelta(weeks=1)
            elif period == PaymentPeriod.MONTHLY:
                next_payment_date = now + timedelta(days=DAYS_IN_SUBSCRIPTION_MONTH)

        await state.update_data(payment_date=next_payment_date)

        await message.answer(
            text=localize_text('messages.create_comment'),
            reply_markup=get_cancel_keyboard()
        )
        await state.set_state(CreateGroupStates.GET_COMMENT)
    except ValueError:
        await message.answer(localize_text('errors.invalid_date'))


@router.message(CreateGroupStates.GET_COMMENT)
async def process_group_comment(message: types.Message, state: FSMContext):
    """Обробка коментаря та завершення створення групи"""
    await state.update_data(comment=message.text)
    await state.update_data(join_id=generate_join_id())

    group = await get_localized_group(state)
    result = localize_text('messages.confirm_create', group=group)

    await message.answer(result, reply_markup=get_confirm_keyboard())
    await state.set_state(CreateGroupStates.CONFIRM)


@router.callback_query(CreateGroupStates.CONFIRM, F.data.in_(['yes']))
async def confirm_create(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору періоду оплати з кнопок"""
    try:
        data = await state.get_data()

        username = callback.from_user.username
        full_name = callback.from_user.full_name
        user_id = callback.from_user.id
        owner_tag = f"@{username}" if username else full_name or str(user_id)

        obj: GroupModel = GroupModel.from_dict({
                "name": data["name"],
                "owner_id": int(callback.from_user.id),
                "owner_tag": owner_tag,
                "description": data.get("comment"),
                "amount": float(data.get("amount", 0)),
                "payment_period": PaymentPeriod[data.get("period", "MONTHLY").upper()],
                "payment_method": PaymentMethod[data.get("method", "EACH_USER").upper()],
                "next_payment_date": data.get("payment_date"),
                "join_id": data.get('join_id'),
        })

        res_id = await create_group_with_custom_join_id(obj)
        if res_id:
            group = await get_localized_group(state)

            await callback.message.answer(
                localize_text('messages.created', group=group),
                reply_markup=get_main_keyboard()
            )

            await callback.answer()
            await callback.message.edit_reply_markup()
            await state.clear()
    except Exception as e:
        print(e)



@router.callback_query(CreateGroupStates.CONFIRM, F.data.in_(['no']))
async def decline_create(callback: CallbackQuery, state: FSMContext):
    """Обробка вибору періоду оплати з кнопок"""
    await state.clear()
    await callback.answer()
    await callback.message.edit_reply_markup()

    await callback.message.answer(
        localize_text('messages.canceled'),
        reply_markup=get_main_keyboard()
    )


async def get_localized_group(state: FSMContext) -> str:
    data = await state.get_data()
    return localize_text(
        'messages.group_admin',
        name=data['name'],
        date=get_displayed_date(data['payment_date']),
        user_count='1',
        sum=data['amount'],
        status='1/1',
        period=localize_text(f"buttons.{data['period']}"),
        period_order=localize_text(f"buttons.{data['period_order']}"),
        comment=data['comment'],
        id=data['join_id']
    )