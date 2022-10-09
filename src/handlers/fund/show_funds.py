from aiogram.types import Message

import db
import texts
import json
import custom_filters

async def get_funds(message: Message):
    list_of_funds = await db.get_all_funds()
    if list_of_funds:
        text = """<b>Фонди 
Кавуневої Республіки</b>\n"""
        for fund in list_of_funds:
            user_tag = await db.get_passport(id = int(fund[1]))
            text = text + f'''
🏦: <b>{fund[3]}</b>
#️⃣  <code>{fund[0]}:{int(fund[1])}</code>
👤 : <a href='t.me/{str(user_tag[3]).split('@')[1]}'>{user_tag[0]} {user_tag[1]}</a>
            '''
        await message.reply(text)
    else:
        await message.reply(f'Поки фондів немає') 
        
async def get_fund(message: Message):
    
    command, fund_id, *all = message.text.split()
    
    fund_id = fund_id[0]
    
    fund = await db.get_fund_by_id(fund_id=fund_id)
    
    if fund:
        
        
        text = f"""
<b>Фонд
Кавуневої Республіки
        """ 
        
        for line in fund: 
            user_tag = await db.get_passport(id = int(line[1]))
            text = text + f"""
🏦 <b>{line[3]}</b>
#️⃣ <code>{line[0]}:{int(line[1])}</code>
👤 <a href='t.me/{str(user_tag[3]).split('@')[1]}'>{user_tag[0]} {user_tag[1]}</a>
💰 <b>{line[2]} чорних злотих</b>
</b>
"""
            have_access = '🏵️ <b>Мають доступ: </b>'
            for user in json.loads(line[4]):
                user = await db.get_passport(user)
                have_access = have_access + f"<a href='t.me/{str(user[3]).split('@')[1]}'>{user[0]} {user[1]}</a>, "
                
            text = text + str(have_access)[:-2]
        await message.answer(text)
    else:
        await message.answer('<b>Такого фонду не існує!</b>')
