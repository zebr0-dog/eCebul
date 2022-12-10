from . import base_db, fund, party, passport, vote, admins, centra_bank

class DataBase(
    admins.AdminsDB,
    centra_bank.CentraBankDB,
    vote.VoteDB,
    fund.FundDB,
    party.PartyDB,
    passport.PassportDB,
    base_db.DB
):
    pass