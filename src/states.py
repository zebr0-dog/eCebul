from aiogram.dispatcher.filters.state import State, StatesGroup

class Register(StatesGroup):
    pass_application = State()

class GivePassport(StatesGroup):
    id_pass = State()
    name_pass = State()
    surname_pass = State()
    sex_pass = State()
    birthdate_pass = State()
    username_pass = State()
    balance_pass = State()
    info_pass = State()
    job_pass = State()
    create_pass_log = State()

class DeletePassport(StatesGroup):
    delete_pass = State()

class ChangePasspost(StatesGroup):
    column_pass = State()
    id_pass = State()
    change_data_pass = State()

class Pay(StatesGroup):
    id = State()
    sum = State()

class RegisterParty(StatesGroup):
    party_application = State()

class CreateParty(StatesGroup):
    id = State()
    name = State()
    id_1 = State()
    id_2 = State()

class AddMember(StatesGroup):
    id = State()

class DeleteMember(StatesGroup):
    id = State()

class RegCandidate(StatesGroup):
    program = State()

class CreateFund(StatesGroup):
    fund_owner_id = State()
    fund_name = State()
    fund_balance = State()
    
class CreateShop(StatesGroup):
    shop_owner_id = State()
    shop_title = State()
    shop_items_num = State() 
    default_message = State()

class CreateItem(StatesGroup):
    shop_id = State()
    item_name = State()
    item_count = State()
    description = State()
    item_cost = State()
    item_status = State()
