from dataclasses import dataclass
from enum import Enum

@dataclass
class Passport:
    id: int
    name: str
    surname: str
    sex: int
    username: str
    balance: int
    status: int
    job: int
    emoji: str
    partner: int
    is_citizen: bool
    passport_photo: str
    birthdate: str

@dataclass
class Diploma:
    user_id: int
    student_name: str
    student_surname: str
    academy_name: str
    date_course_start: str
    date_course_end: str
    average_grade: int

@dataclass
class Fund:
    id: int
    owner: int
    balance: int
    name: str

@dataclass
class Personal:
    id: int
    can_withdraw: bool
    can_add_personal: bool

@dataclass
class Party:
    id: int
    name: str
    owner: int

@dataclass
class Member:
    id: int
    name: str
    surname: str
    can_add_members: bool

@dataclass
class Candidate:
    id: int
    name: str
    surname: str
    username: str
    party: str
    program: str
    votes: int

@dataclass
class Admin:
    id: int
    chat: int
    can_mute: bool
    can_ban: bool
    can_pin: bool
    can_manage_money: bool
    can_manage_partyies: bool
    can_give_passports: bool
    can_promote: bool
    can_give_diplomas: bool

class StatusOfVoting(Enum):
    NO_VOTING = 1
    REGISTER_OF_CANDIDATES = 2
    VOTING = 3
