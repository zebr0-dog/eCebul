WELCOME_CHAT_MESSAGE = """
Вітаємо в {chat}, <a href="tg://user?id={id}">{name}</a>.
Будь-ласка натисніть {number} кнопку.
"""

FORM_TEXT= """
<b>Натисніть на форму нижче, заповніть її та надішліть результати.</b>

<code>
Ім'я:
Прізвище:
Стать: Чоловік або Жінка
Дата народження: рік, місяць і день
</code>


<b>Форму треба заповнити правильно, інакше ваше звернення не буде опрацьовано!</b>
"""

FORM_PARTION_TEXT = """
Вітаю. Для створення партії напишіть, будь-ласка, наступну заяву:
<code>Я, [ім'я прізвище в паспорті], звертаюсь до вас з проханням \
    узгодити створення та реєстрацію моєї політичної партії —  "[Назва партії]".
Одразу прошу додати до списку партійців наступних носіїв громадянства:
@тег1
@тег2</code>

Для створення партії треба як мінімум 2 людини окрім Вас.
"""

NEW_REQUEST = """
<b>Нова заявка</b>

{text}
ID: {id}
Юзернейм: @{username}

<b>Відповідь на заявку треба робити у Приватних Повідомленнях!</b>"""

WARNING_ALERT = """
<b>
Уважно слідкуйте за моїми повідомленнями, та відповідайте на поставлені запитання!
</b>
"""

FIRST_STEP = """
<b>
Перший крок оформлення:

Надішліть ID користувача.
</b>"""
SECOND_STEP = """
<b>
Другий крок оформлення:

Надішліть Ім'я користувача
</b>"""
THIRD_STEP = """
<b>
Третій крок оформлення:

Надішліть Прізвище користувача.
</b>"""

FOURTH_STEP = """<b>
Четвертий крок оформлення:

Оберіть Стать користувача.
</b>"""
FIVETH_STEP = """<b>
П'ятий крок оформлення:

Вкажіть ТЕГ користувача.
</b>"""
SIXTH_STEP = """<b>
Шостий крок оформлення:

Вкажіть дату народження користувача (у форматі "рік-місяць-день").
</b>"""
SEVENTH_STEP = """💰 <b>Встановіть баланс для користувача</b>"""

PASSPORT_WAS_GIVEN = """
<b>
Реєстратор схвалив вашу заявку!

Для перевірки вашого профілю введіть !пас
</b>"""

PASSPORT = """
<b>ПАСПОРТ КАВУНЕВОЇ РЕСПУБЛІКИ</b>

{emoji} {name} {surname}
🆔 <code>К{id}Р</code>
🚻 {sex}
📅 {birthdate}, {yearsold} років
🌐 <a href="t.me/{username}">Ідентифікатор</a>

📌 {is_citizen}
💼 {job}

💍 {partner}

{info}
"""

DIPLOMATIC_PASSPORT = """
<b>ДИПЛОМАТИЧНИЙ ПАСПОРТ КАВУНЕВОЇ РЕСПУБЛІКИ
DIPLOMATIC PASSPORT OF KAVUNIAN REPUBLIC
PASSEPORT DIPLOMATIQUE DE LA KAVUN REPUBLIQUE</b>

{emoji} {name} {surname}
🆔 <code>К{id}Р</code>
🚻 {sex}
📅 {birthdate}, {years_old} років
"""

DIPLOMA = """
<b>ДИПЛОМ {academy_name}</b>

👤 {student_name} {student_surname}
🆔 <code>К{user_id}Р</code>

📅 {date_course_start}
📅 {date_course_end}

💯 {average_grade}/100
"""

BANK_ACCOUNT = """
<b>ДЕРЖАВНИЙ БАНК 
Кавуневої Республіки</b>

💳 <a href="t.me/{username}">Рахунок</a>
💰 Баланс: {balance} чорних злотих
"""

FUND = """
🏦: <b>{fund_name}</b>
#️⃣: <code>{fund_id}:{fund_owner_id}</code>
👤: <a href='t.me/{owner_username}'>{owner_name} {owner_surname}</a>
"""

FUND_DETAILED = """
<b>Фонд Кавуневої Республіки</b>

🏦 <b>{name}</b>
#️⃣ <code>{id}:{owner}</code>
👤 <a href='t.me/{username}'>{owner_name} {surname}</a>
💰 <b>{balance} чорних злотих</b>

🏵️ <b>Мають доступ: </b>
"""

PARTYIES = {
    1: """
📄 {name}
👑 <a href="t.me/{username}">{owner_name} {owner_surname}</a>
👤 Учасників: {members_count}
"""
}

PASSPORT_DO_NOT_EXIST = "<b>У вас немає паспорту. Будь ласка, звернітися до МВС для отримання паспорту.</b>"

CHANGE_PASSPORT = "<b>Що саме ви хочете змінити?</b>"

REQUEST_ID = """
<b> Кому змінюємо {column}?

Надішліть ID користувача.</b>"""

RESTRICT_TEXT = """
Адміністратор: <a href="tg://?id={admin_id}">{admin_first_name}</a>
Замутив: <a href="tg://user?id={target_id}">{target_first_name}</a>
Термін: {mute_time} {mute_type}

Коментар: {comment}"""

UNRESTRICT_TEXT = """
Адміністратор: <a href="tg://?id={admin_id}">{admin_first_name}</a>
Розмутив: <a href="tg://user?id={target_id}">{target_first_name}</a>"""

BAN_TEXT = """
Адміністратор: <a href="tg://?id={admin_id}">{admin_first_name}</a>
Забанив: <a href="tg://user?id={target_id}">{target_first_name}</a>
Термін: назавжди

Коментар: {comment}"""

UNBAN_TEXT = """
Адміністратор: <a href="tg://?id={admin_id}">{admin_first_name}</a>
Розбанив: <a href="tg://user?id={target_id}">{target_first_name}</a>"""

REGISTRATION_WAS_STARTED = """📢 Розпочалась реєстрація кандидатів на чергові вибори 

Щоб приймати участь у виборах, перейдіть в бота і зареєструйтесь <code>!балотуватись</code>. 

‼️ Важливо, для балотування треба власна програма та статус Середняка"""

VOTING_WAS_STARTED = """🗳️ Розпочалися чергові вибори

Для голосування перейдіть в бота і введіть команду <code>!голосувати</code>

‼️ Голосувати можуть лише особи зі статусом Середняк та вище"""

FINAL_RES = """🗳️ Результати чергових виборів

👤 <a href="t.me/{username}">{name} {surname}</a>
✉️ Кількість голосів: {votes}"""

CANDIDAT_PROFILE = """👤 <a href="t.me/{username}">{name} {surname}</a>
🖼️ {party}

{program}"""

PROPOSAL_TEXT = """<a href="t.me/{}">Користувач</a> запропонував вам вступити в шлюб"""

MARRIAGE_RESULTS = {
    0: "Шлюб успішно укладено",
    1: "Хтось з партнерів вже в шлюбі",
    2: "Одностатеві шлюби заборонені",
    3: "Хтось з партнерів не є громадянином Республіки"
}
DIVORCE_RESULTS = {
    0: "Шлюб розірвано",
    1: "Ви не є законними партнерами"
}

DIPLOMA_REGISTRATION_STEPS = {
    0: "Надішлить id студента - ",
    1: "Ім'я вашого студента - ",
    2: "Призвище вашого студента - ",
    3: "Назву вашого навчального закладу - ",
    4: "Дату початку курсу (yyyy-mm-dd) - ",
    5: "Дату закінчення курса (yyyy-mm-dd) - ",
    6: "Середний бал - "
}

DIPLOMA_DO_NOT_EXIST = """<b>У вас немає диплому. Звернітеся до Міністерства Освіти для отримання диплому.</b>"""
DIPLOMA_WAS_GIVEN = """<b>Вітаємо. Вам був видан диплом.</b>"""
DIPLOMATIC_PASSPORT_DO_NOT_EXIST = """<b>У вас немає дипломатичного паспорту. Звернітеся до МВС для отримання диппаспорту.</b>"""
