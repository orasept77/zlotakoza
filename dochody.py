import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import exceptions
from categories import Categories


class Message(NamedTuple):
    amount: int
    category_text: str


class Dochod(NamedTuple):
    id: Optional[int]
    amount: int
    category_name: str


def add_dochod(raw_message: str) -> Dochod:
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert("dochod", {
        "amount": parsed_message.amount,
        "created": _get_now_formatted(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Dochod(id=None,
                  amount=parsed_message.amount,
                  category_name=category.name)


def get_today_statistics() -> str:
    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   "from dochod where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Dziszaj nie masz dochodów"
    all_today_dochody = result[0]
    cursor.execute("select sum(amount) "
                   "from dochod where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_dzieny_dochod=true)")
    result = cursor.fetchone()
    base_today_dochody = result[0] if result[0] else 0
    return (f"Dochodę za dziszaj:\n"
            f"razem — {all_today_dochody} zł.\n"
            f"minimalne — {base_today_dochody} zł. z {_get_dochod_dzieny()} zł.\n\n"
            f"za miesząc: /month")


def get_month_statistics() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from dochod where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "Wprawie nie masz dochodów"
    all_today_dochody = result[0]
    cursor.execute(f"select sum(amount) "
                   f"from dochod where date(created) >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_dzieny_dochod=true)")
    result = cursor.fetchone()
    base_today_dochody = result[0] if result[0] else 0
    return (f"Dochód za mięsziąc:\n"
            f"Razem — {all_today_dochody} zł.\n"
            f"Minimalne — {base_today_dochody} zł. z "
            f"{now.day * _get_dochod_dzieny()} zł.")


def last() -> List[Dochod]:
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name "
        "from dochod e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_dochody = [Dochod(id=row[0], amount=row[1], category_name=row[2]) for row in rows]
    return last_dochody


def delete_dochod(row_id: int) -> None:
    db.delete("dochod", row_id)


def _parse_message(raw_message: str) -> Message:
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Nie rozumiem, napisz"
            "naprzykład:\n150 młęko")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_formatted() -> str:
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")


def _get_now_datetime() -> datetime.datetime:
    tz = pytz.timezone("Poland")
    now = datetime.datetime.now(tz)
    return now


def _get_dochod_dzieny() -> int:
    return db.fetchall("dochod_dzieny", ["dochod_dzien"])[0]["dochod_dzien"]
