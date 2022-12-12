from typing import Dict
from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton
)
from aiogram.utils.callback_data import CallbackData

import variables

from models import Candidate

captcha_cb = CallbackData("cap", "answer")
party_select = CallbackData("sel", "act")
party = CallbackData("par", "act")
candidates_cb = CallbackData("can", "id")
vote_cb = CallbackData("vote", "id")
marriage_cb = CallbackData("marr", "id1", "id2")
permission_cb = CallbackData("perm", "id", "num", "active")

def sex_keyboard():
    sex_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Чоловік")
            ],
            [
                KeyboardButton(text="Жінка")
            ],
            
        ],
        resize_keyboard=True
    )
    return sex_menu

def citizenship_keyboard():
    citizenship_menu = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Громадянин")
            ],
            [
                KeyboardButton(text="Негромадянин")
            ],
        ],
        resize_keyboard=True
    )
    return citizenship_menu

def job_keyboard():
    job_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for job in variables.JOBS.keys():
        job_kb.add(KeyboardButton(text=job))
    return job_kb

def status_keyboard():
    status_kb = ReplyKeyboardMarkup(
        resize_keyboard=True
    )
    for status in variables.STATUSES.keys():
        status_kb.add(status)
    return status_kb

def dicise_party(owner: int):
    dis = InlineKeyboardMarkup(row_width=2)
    dis.insert(InlineKeyboardButton(
        "Прийняти",
        callback_data=party_select.new(
            act="yes_"+str(owner)
        ))
    )
    dis.insert(InlineKeyboardButton(
        "Відхилити",
        callback_data=party_select.new(
            "no_"+str(owner)
        ))
    )
    return dis

def party_manage_keyboard(is_owner: bool):
    if is_owner:
        party_manage = InlineKeyboardMarkup(row_width=1)
        party_manage.add(InlineKeyboardButton(
            "Додати учасника",
            callback_data=party.new(act="add")
        ))
        party_manage.add(InlineKeyboardButton(
            "Видалити учасника",
            callback_data=party.new(act="delete")
        ))
        return party_manage
    else:
        return

def change_kb_gen(allowed_changes=variables.ALLOWED_CHANGES):
    change_kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        row_width=1,
        input_field_placeholder="Оберіть поле для зміни"
    )
    for change in allowed_changes:
        change_kb.add(KeyboardButton(text=change))
    return change_kb

def gen_captcha_keyboard(correct, user_id):
    captcha = InlineKeyboardMarkup(row_width=1)
    for i in range(1, 5):
        if i != correct:
            captcha.add(InlineKeyboardButton(
                "Слава Кавуну",
                callback_data=captcha_cb.new(
                    answer="wrong_"+str(user_id)
                ))
            )
        else:
            captcha.add(InlineKeyboardButton(
                "Слава Кавуну",
                callback_data=captcha_cb.new(
                    answer="correct_"+str(user_id)
                ))
            )
    return captcha

def candidates_keyboard(candidates: Dict[int, Candidate]):
    keyb = InlineKeyboardMarkup(row_width=1)
    for id, candidate in candidates.items():
        keyb.add(InlineKeyboardButton(
            " ".join([
                    candidate.name,
                    candidate.surname
                ]),
            callback_data=candidates_cb.new(id=str(candidate.id))
        ))
    return keyb

def vote(id: int):
    str_id = str(id)
    keyb = InlineKeyboardMarkup()
    keyb.add(InlineKeyboardButton("Проголосувати", callback_data=vote_cb.new(id=str_id)))
    return keyb

def marriage_buttons(id1, id2):
    id1, id2 = str(id1), str(id2)
    keyb = InlineKeyboardMarkup(row_width=2)
    keyb.add(
        InlineKeyboardButton("Прийняти", callback_data=marriage_cb.new(id1, id2)),
        InlineKeyboardButton("Відхилити", callback_data=marriage_cb.new("0", id2))
    )
    return keyb

def permission_buttons(id: int, **kwargs):
    keyb = InlineKeyboardMarkup(row_width=3)
    indexes = {
        1: "Мут",
        2: "Бан",
        3: "Пін",
        4: "Партії",
        5: "Гроші",
        6: "Паспорти", 
        7: "Назначати",
        8: "Глобальні права",
        9: "Діпломи"
    }
    emojies = {
        0: "❌",
        1: "✅"
    }
    for i in range(1, 10):
        active = kwargs.get(str(i), 0)
        text = emojies.get(int(active), "") + indexes.get(i, "Error")
        keyb.insert(
            InlineKeyboardButton(text, callback_data=permission_cb.new(id=id, num=i, active=active)),
        )
    keyb.add(
        InlineKeyboardButton("Зберегти", callback_data=permission_cb.new(id=id, num=10, active=0)),
    )
    return keyb
