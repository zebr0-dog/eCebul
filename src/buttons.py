from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton
)

start_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Звичайно!")
        ],
        
    ],
    resize_keyboard=True
)

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

complete = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Затвердити!")
        ],
        
    ],
    resize_keyboard=True
)

balance_reg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="0")
        ],
        
    ],
    resize_keyboard=True
)  

job_reg = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Безробітній")
        ],
        [
            KeyboardButton(text='Президент')
        ],
        [
            KeyboardButton(text='Спікер')
        ], 
        [
            KeyboardButton(text='Віце-Спікер')
        ], 
        [
            KeyboardButton(text='Чатовий')
        ], 
        [
            KeyboardButton(text='Жандарм')
        ], 
        [
            KeyboardButton(text='Депутат')
        ], 
        [
            KeyboardButton(text='Міністр Внутрішніх Справ')
        ],
        [
            KeyboardButton(text='Міністр Оборони')
        ],
        [
            KeyboardButton(text='Міністр Економіки')
        ],
        [
            KeyboardButton(text='Верховний Суддя')
        ],
        [
            KeyboardButton(text='Помічник Судді')
        ],
        [
            KeyboardButton(text='Апеляційний Суддя')
        ]
    ],
    resize_keyboard=True
)

change_info = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="❌ Відсторонений, не має впливу на Державу")
        ],
        [
            KeyboardButton(text="🪆 Новачок, тільки приєднався до Держави!")
        ],
        [
            KeyboardButton(text="🎗️ Середняк, розуміє головні Державні аспекти!")
        ],
        [
            KeyboardButton(text="🎖️ Ветеран, знається на Державі")
        ],
        
    ],
    resize_keyboard=True
)

def change_kb_gen(lor: int):
    change_kb = ...
    if lor == 5:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ім'я")
                ],
                [
                    KeyboardButton(text="прізвище")
                ],
                [
                    KeyboardButton(text="стать")
                ],
                [
                    KeyboardButton(text="тег")
                ],
                [
                    KeyboardButton(text="баланс")
                ],
                [
                    KeyboardButton(text="інфо")
                ],
                [
                    KeyboardButton(text="робота")
                ],
            ],
            resize_keyboard=True
        )
    elif lor == 4:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="ім'я")
                ],
                [
                    KeyboardButton(text="прізвище")
                ],
                [
                    KeyboardButton(text="стать")
                ],
                [
                    KeyboardButton(text="тег")
                ],
                [
                    KeyboardButton(text="інфо")
                ],
                [
                    KeyboardButton(text="робота")
                ],
            ],
            resize_keyboard=True
        )
    elif lor == 3:
        change_kb = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="баланс")
                ],
            ],
            resize_keyboard=True
        )
    return change_kb

def gen_captcha_keyboard(correct):
    captcha = InlineKeyboardMarkup(row_width=1)
    for i in range(1, 5):
        if i != correct:
            captcha.add(InlineKeyboardButton("Слава Цибулі", callback_data="wrong"))
        else:
            captcha.add(InlineKeyboardButton("Слава Цибулі", callback_data="correct"))
    return captcha