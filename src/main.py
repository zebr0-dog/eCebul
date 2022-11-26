import logging
import os
import dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# init logging, bot and dispatcher. Load env vars

dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
MAIN_CHAT = int(os.getenv("MAIN_CHAT"))
LOG_CHANNEL = int(os.getenv("LOGS"))
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML, disable_web_page_preview=True)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

if __name__ == "__main__":
    
    # imports modules

    import handlers
    import custom_filters
    import states
    from db import create_table
    from buttons import party, party_select, captcha_cb, candidates_cb, vote_cb, marriage_cb

    # bound filter

    dp.filters_factory.bind(custom_filters.isPassportExist)
    dp.filters_factory.bind(custom_filters.levelOfRight)
    
    # registration of handlers
    
    dp.register_message_handler(
        handlers.passport.register_passport.cancel_giving,
        commands="скасувати",
        commands_prefix="!",
        state="*",
        chat_type="private"
    )
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
        handlers.navigation.navig,
        commands="навігатор",
        commands_prefix="!"
    )
    # dp.register_message_handler(
    #     handlers.shop.view_shop.shop_view,
    #     commands="магазин",
    #     commands_prefix="!"
    # )
    # dp.register_message_handler(
    #     handlers.shop.view_item.my_items,
    #     commands="предмети",
    #     commands_prefix="!"
    # )
    dp.register_message_handler(
        handlers.vote.candidates.candidats,
        level_of_right=3,
        commands=["slaves", "кандидати"],
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.party.show_partyies.show_partyies,
        commands="партії",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.party.edit_partyies.party_profile,
        chat_type="private",
        commands="партія",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.party.create_party.reg_party,
        chat_type="private",
        commands="створити",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.party.create_party.registration,
        state=states.RegisterParty.party_application
    )
    dp.register_message_handler(
        handlers.money.pay_by_reply,
        is_reply=True,
        commands="переказати",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.money.pay_by_id,
        chat_type="private",
        commands="переказати",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.vote.reg_candidate.start_reg,
        is_passport_exist=True,
        chat_type="private",
        commands="балотуватись",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.vote.reg_candidate.get_program,
        is_passport_exist=True,
        chat_type="private",
        state=states.RegCandidate.program
    )
    dp.register_message_handler(
        handlers.vote.voting.list_of_candidats,
        is_passport_exist=True,
        chat_type="private",
        commands="голосувати",
        commands_prefix="!",
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
    dp.register_message_handler(
        handlers.party.edit_partyies.get_id_for_add,
        chat_type="private",
        state=states.AddMember.id
    )
    dp.register_message_handler(
        handlers.party.edit_partyies.get_id_for_delete,
        chat_type="private",
        state=states.DeleteMember.id
    )
    dp.register_callback_query_handler(
        handlers.moderation.check,
        captcha_cb.filter()
    )
    dp.register_callback_query_handler(
        handlers.party.edit_partyies.yes,
        party_select.filter(),
        lambda cb: "yes" in cb.data,
        chat_type="private",
    )
    dp.register_callback_query_handler(
        handlers.party.edit_partyies.no,
        party_select.filter(),
        lambda cb: "no" in cb.data,
        chat_type="private",
    )
    dp.register_callback_query_handler(
        handlers.vote.voting.get_candidat_info,
        candidates_cb.filter(),
        chat_type="private",
    )
    dp.register_callback_query_handler(
        handlers.vote.voting.vote,
        vote_cb.filter(),
        chat_type="private",
    )
    dp.register_callback_query_handler(
        handlers.party.edit_partyies.add_member,
        party.filter(act="add"),
        chat_type="private",
    )
    dp.register_callback_query_handler(
        handlers.party.edit_partyies.delete_member,
        party.filter(act="delete"),
        chat_type="private",
    )
    dp.register_message_handler(
        handlers.marriage.marry.marriage_proposal,
        is_reply=True,
        commands="шлюб",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.marriage.divorce.divorce_process,
        is_reply=True,
        commands="розлучення",
        commands_prefix="!",
    )
    dp.register_callback_query_handler(
        handlers.marriage.marry.marriage_declined,
        marriage_cb.filter(id1="0")
    )
    dp.register_callback_query_handler(
        handlers.marriage.marry.marriage_accepted,
        marriage_cb.filter()
    )
    # dp.register_callback_query_handler(
    #     handlers.shop.callbacks.shopes
    # )
    # adm
    dp.register_message_handler(
        handlers.passport.show_passports.show_pass_admin,
        is_reply=True,
        level_of_right=1,
        commands=["документи", "док"],
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.fund.create_fund.create_fund,
        chat_type="private",
        level_of_right=3,
        commands="створити_фонд",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.fund.create_fund.get_fund_owner_id,
        state=states.CreateFund.fund_owner_id
    )
    dp.register_message_handler(
        handlers.fund.create_fund.get_fund_name,
        state=states.CreateFund.fund_name
    )
    dp.register_message_handler(
        handlers.fund.create_fund.get_fund_balance,
        state=states.CreateFund.fund_balance
    )
    dp.register_message_handler(
        handlers.fund.show_funds.get_funds,
        commands="фонди",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.fund.show_funds.get_fund,
        commands="фонд",
        commands_prefix="!"
    )
    dp.register_message_handler(
        handlers.fund.fund_managment.add_manager,
        commands="додати_у_фонд",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.fund.fund_managment.delete_manager,
        commands="видалити_з_фонду",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.fund.delete_fund.delete_fund,
        level_of_right=3,
        commands="видалити_фонд",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.fund.fund_managment.withdraw_money,
        level_of_right=3,
        commands="списати",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.fund.fund_managment.take_money,
        commands="зняти",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.fund.fund_managment.replenish_fund,
        commands="поповнити",
        commands_prefix="!",
        chat_type="private"
    )
    dp.register_message_handler(
        handlers.passport.show_passports.find_pass_admin,
        level_of_right=1,
        commands="знайти",
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
            "робота",
            "емодзі"
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
        level_of_right=5,
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
    dp.register_message_handler(
        handlers.party.create_party.create_party_start,
        level_of_right=3,
        commands="зареєструвати",
        commands_prefix="!",
        chat_type="private",
    )
    dp.register_message_handler(
        handlers.party.create_party.get_id,
        state=states.CreateParty.id
    )
    dp.register_message_handler(
        handlers.party.create_party.get_name,
        state=states.CreateParty.name
    )
    dp.register_message_handler(
        handlers.party.create_party.get_first_tag,
        state=states.CreateParty.id_1
    )
    dp.register_message_handler(
        handlers.party.create_party.get_second_tag,
        state=states.CreateParty.id_2
    )
    dp.register_message_handler(
        handlers.vote.admins.start_reg_candidats,
        is_passport_exist=True,
        level_of_right=4,
        chat_type="private",
        commands="реєстрація",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.vote.admins.start_voting,
        is_passport_exist=True,
        level_of_right=4,
        chat_type="private",
        commands="голосування",
        commands_prefix="!",
    )
    dp.register_message_handler(
        handlers.vote.admins.final_voting,
        is_passport_exist=True,
        level_of_right=4,
        chat_type="private",
        commands="фінал",
        commands_prefix="!",
    )



    executor.start_polling(dp, skip_updates=True, on_startup=create_table)
