import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        count = 0
        date = dt.datetime.now().date()
        for every_record in self.records:
            if every_record.date == date:
                count += every_record.amount
        return count

    def get_week_stats(self):
        count_week = 0
        date_today = dt.datetime.now().date()
        date_week_ago = date_today - dt.timedelta(days=7)
        for every_record in self.records:
            if date_week_ago < every_record.date <= date_today:
                count_week += every_record.amount
        return count_week


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    USD_RATE = float(75)
    EURO_RATE = float(92)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency):
        currency_map = {'usd': self.USD_RATE,
                        'eur': self.EURO_RATE,
                        'rub': self.RUB_RATE
                        }

        currency_transform_string_map = {
            'usd': 'USD',
            'eur': 'Euro',
            'rub': 'руб'
        }

        remainder = self.limit - self.get_today_stats()
        remained = round(float(remainder / currency_map[currency]), 2)
        if remainder == 0:
            return 'Денег нет, держись'
        elif remainder > 0:
            return f'На сегодня осталось ' \
                   f'{remained} {currency_transform_string_map[currency]}'
        else:
            return f'Денег нет, держись: твой долг - {abs(remained)} ' \
                   f'{currency_transform_string_map[currency]}'


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        count_calories = self.get_today_stats()
        if count_calories < self.limit:
            return f'Сегодня можно съесть что-нибудь ещё, ' \
                   f'но с общей калорийностью не более' \
                   f' {self.limit - count_calories} кКал'
        else:
            return "Хватит есть!"


# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(1000)

# дата в параметрах не указана,
# так что по умолчанию к записи
# должна автоматически добавиться сегодняшняя дата
cash_calculator.add_record(Record(amount=145, comment='кофе'))
# и к этой записи тоже дата должна добавиться автоматически
cash_calculator.add_record(Record(amount=300, comment='Серёге за обед'))
# а тут пользователь указал дату, сохраняем её
cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др', date='08.11.2019'))

print(cash_calculator.get_today_cash_remained('rub'))
# должно напечататься
# На сегодня осталось 555 руб
