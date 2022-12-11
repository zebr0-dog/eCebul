import operator


JOBS = {
    "Безробітній": 0,
    "Президент": 1,
    "Спікер": 2,
    "Віце-Спікер": 3,
    "Чатовий": 4,
    "Жандарм": 5,
    "Депутат": 6,
    "Міністр Внутрішніх Справ": 7,
    "Міністр Освіти": 8,
    "Міністр Закордонних Справ": 9,
    "Міністр Оборони": 10,
    "Міністр Економіки": 11,
    "Голова Центрального Банку": 12,
    "Слідчий": 13,
    "Посол": 14,
    "Верховний Суддя": 15,
    "Помічник Судді": 16,
    "Апеляційний Суддя": 17,
    "Персонал Центрального Банку": 18
}

JOBS_REVERSED = {v: k for k, v in JOBS.items()}

STATUSES = {
    "❌ Відсторонений, не має впливу на Державу": 0,
    "🪆 Новачок, тільки приєднався до Держави!": 1,
    "🎗️ Середняк, розуміє головні Державні аспекти!": 2,
    "🎖️ Ветеран, знається на Державі": 3
}

STATUSES_REVERSED = {v: k for k, v in STATUSES.items()}

SEX = {
    0: "Чоловік",
    1: "Жінка"
}

SEX_REVERSED = {v: k for k, v in SEX.items()}

ALLOWED_CHANGES = [
    "ім'я",
    "прізвище",
    "стать",
    "тег",
    "баланс",
    "статус",
    "громадянство",
    "робота",
    "емодзі",
    "дата_народження"
]

OPERATORS = {
    "+": operator.add,
    "-": operator.sub,
    "=": operator.eq,
}
