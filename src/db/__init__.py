from . import base_db, fund, party, passport, vote, admins, centra_bank, diploma

class DataBase(
    admins.AdminsDB,
    centra_bank.CentraBankDB,
    vote.VoteDB,
    fund.FundDB,
    party.PartyDB,
    passport.PassportDB,
    diploma.DiplomaDB,
    base_db.DB
):
    pass
