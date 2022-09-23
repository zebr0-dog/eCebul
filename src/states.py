from aiogram.dispatcher.filters.state import State, StatesGroup

class Register(StatesGroup):
    pass_application = State()

class GivePassport(StatesGroup):
    id_pass = State()
    name_pass = State()
    surname_pass = State()
    sex_pass = State()
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