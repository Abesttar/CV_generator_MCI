from datetime import date

def format_japanese_date(dt):
    return f"{dt.year}年{dt.month}月{dt.day}日"

def calculate_age(birth_date):
    today = date.today()

    age = (
        today.year
        - birth_date.year
        - (
            (today.month, today.day)
            < (birth_date.month, birth_date.day)
        )
    )

    return age

def format_phone(phone):
    phone = str(phone).replace("+62", "")
    return f"+62{phone}"