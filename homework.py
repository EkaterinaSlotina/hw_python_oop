import datetime as dt
FORMAT_DATE = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, FORMAT_DATE).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        date_today = dt.date.today()
        count = sum(record.amount for record in self.records
                    if record.date == date_today)
        return count

    def get_week_stats(self):
        date_today = dt.date.today()
        date_week_ago = date_today - dt.timedelta(days=7)
        count_week = sum(record.amount for record in self.records
                         if date_week_ago < record.date <= date_today)
        return count_week

    def remained(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = float(75)
    EURO_RATE = float(92)
    RUB_RATE = float(1)

    def get_today_cash_remained(self, currency):
        currency_map = {'usd': (self.USD_RATE, 'USD'),
                        'eur': (self.EURO_RATE, 'Euro'),
                        'rub': (self.RUB_RATE, 'руб')}
        if currency not in currency_map:
            return 'Введите другую валюту. Данная валюта не поддерживается'
        remained = self.remained()
        if remained == 0:
            return 'Денег нет, держись'
        rate, symbol = currency_map[currency]
        remained_in_currency = round(float(remained / rate), 2)
        if remained > 0:
            return ('На сегодня осталось '
                    f'{remained_in_currency} {symbol}')
        else:
            remained_in_currency_abs = abs(remained_in_currency)
            return ('Денег нет, держись: твой долг - '
                    f'{remained_in_currency_abs} {symbol}')


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.remained() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.remained()} кКал')
        return "Хватит есть!"

