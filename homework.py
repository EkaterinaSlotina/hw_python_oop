import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
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
        date_today = dt.date.today()
        count = sum(record.amount for record in self.records
                    if record.date == date_today)
        return count

    def get_week_stats(self):
        count_week = 0
        date_today = dt.date.today()
        date_week_ago = date_today - dt.timedelta(days=7)
        for record in self.records:
            if date_week_ago < record.date <= date_today:
                count_week += record.amount
        return count_week

    def remained(self):
        limit_remained = self.limit - self.get_today_stats()
        return limit_remained


class CashCalculator(Calculator):
    USD_RATE = float(75)
    EURO_RATE = float(92)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency):
        currency_map = {'usd': (self.USD_RATE, 'USD'),
                        'eur': (self.EURO_RATE, 'Euro'),
                        'rub': (self.RUB_RATE, 'руб')}
        if self.remained() == 0:
            return 'Денег нет, держись'
        remained = round(float(self.remained() / currency_map[currency][0]), 2)
        if self.remained() > 0:
            return ('На сегодня осталось '
                    f'{remained} {currency_map[currency][1]}')
        else:
            return (f'Денег нет, держись: твой долг - {abs(remained)} '
                    f'{currency_map[currency][1]}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.remained() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.limit - self.get_today_stats()} кКал')
        return "Хватит есть!"


