import logging
import os
from sys import prefix
import dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# init logging, bot and dispatcher. Load env vars

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == "__main__":
    
    # imports modules

    import handlers
    import custom_filters
    import states
    from db import create_table

    # bound filter

    dp.filters_factory.bind(custom_filters.isPassportExist)
    dp.filters_factory.bind(custom_filters.levelOfRight)
    
    # registration of handlers
    
    dp.register_message_handler(
        handlers.passport.show_passports.show_pass,
        is_passport_exist=True,
        commands="start",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.start,
        commands="start",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.registration_msg,
        text="Звичайно!"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.registration,
        state=states.Register.pass_application
    )
    dp.register_message_handler(
        handlers.passport.show_passports.show_pass,
        commands="пас",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.money.pay_by_reply,
        is_reply=True,
        commands="перевести",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.money.pay_by_id,
        commands="перевести",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.money.get_id,
        state=states.Pay.id
    )
    dp.register_message_handler(
        handlers.money.get_sum,
        state=states.Pay.sum
    )
    dp.register_message_handler(
        handlers.moderation.new_member,
        content_types=["new_chat_members"]
    )
    dp.register_message_handler(
        handlers.money.balance,
        commands="баланс",
        commands_prefix="!"
    )
    dp.register_callback_query_handler(
        handlers.moderation.check
    )
    # adm
    dp.register_message_handler(
        handlers.passport.show_passports.show_pass_admin,
        is_reply=True,
        level_of_right=1,
        commands=["документи", "док"],
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.give,
        level_of_right=3,
        commands="видати",
        commands_prefix="!",
        state=None,
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.cancel_giving,
        level_of_right=3,
        commands="скасувати",
        commands_prefix="!",
        state=["*"],
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.citiezinship_was_cancelled,
        level_of_right=3,
        commands="відмова",
        commands_prefix="!",
        state=None,
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_id,
        state=states.GivePassport.id_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_name,
        state=states.GivePassport.name_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_surname,
        state=states.GivePassport.surname_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_sex,
        state=states.GivePassport.sex_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_username,
        state=states.GivePassport.username_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_balance,
        state=states.GivePassport.balance_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_info,
        state=states.GivePassport.info_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.giving_job,
        state=states.GivePassport.job_pass
    )
    dp.register_message_handler(
        handlers.passport.register_passport.registration_logname,
        state=states.GivePassport.create_pass_log
    )
    dp.register_message_handler(
        handlers.passport.edit_passport.change_help,
        level_of_right=3,
        commands="змінити",
        commands_prefix="!",
        chat_type="private",
        state=None
    )
    dp.register_message_handler(
        handlers.passport.edit_passport.change_start,
        text=[
            "ім'я",
            "прізвище",
            "стать",
            "тег",
            "баланс",
            "інфо",
            "робота"
        ],
        state=states.ChangePasspost.column_pass
    )
    dp.register_message_handler(
        handlers.passport.edit_passport.get_id,
        state=states.ChangePasspost.id_pass
    )
    dp.register_message_handler(
        handlers.passport.edit_passport.get_new_data,
        state=states.ChangePasspost.change_data_pass
    )
    dp.register_message_handler(
        handlers.passport.delete_passport.delete_passport_start,
        level_of_right=3,
        commands="видалити",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.passport.delete_passport.delete_passport,
        state=states.DeletePassport.delete_pass
    )
    dp.register_message_handler(
        handlers.moderation.unmute,
        is_reply=True,
        level_of_right=1,
        commands="розмут",
        commands_prefix='!'
    )
    dp.register_message_handler(
        handlers.moderation.ban,
        is_reply=True,
        level_of_right=2,
        commands="бан",
        commands_prefix='!'
    )
    dp.register_message_handler(
        handlers.moderation.unban,
        level_of_right=2,
        is_reply=True,
        commands="розбан",
        commands_prefix='!'
    )
    dp.register_message_handler(
        handlers.moderation.set_admin,
        is_reply=True,
        level_of_right=3,
        commands="назначити",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.moderation.mute,
        is_reply=True,
        level_of_right=1,
        commands=["мут", "mute"],
        commands_prefix='!'
    )

    executor.start_polling(dp, skip_updates=True, on_startup=create_table)