
from project.services.google_finance import GoogleFinance
from decimal import ROUND_HALF_UP, Decimal


class Stock(GoogleFinance):

    def __init__(self, market, ticker):
        super().__init__(market, ticker)

        self.inc = super().income_statement()
        self.bal = super().balance_sheet()
        self.cas = super().cash_flow()
        self.data = super().stock_data()

    def generate_metrics(self):
        data = {}
        data['current_ratio'] = self._compute_current_ratio()
        data['quick_ratio'] = self._compute_quick_ratio()
        data['return_on_equity'] = self._compute_return_on_equity()
        data['debt_equity_ratio'] = self._compute_debt_equity_ratio()
        data['net_profit_margin'] = self._compute_net_profit_margin()
        data['free_cash_flow'] = self._compute_free_cash_flow()
        data['price_to_earnings_ratio'] = self._get_price_to_earnings_ratio()

        if self.data:
            self.data.update(data)

    @staticmethod
    def _round_decimal(number):
        return number.quantize(Decimal('.01'), rounding=ROUND_HALF_UP)

    def _compute_current_ratio(self):
        try:
            if self.bal[10][0] == 'Total Current Assets' and self.bal[23][0] == 'Total Current Liabilities':
                return self._round_decimal(self.bal[10][1] / self.bal[23][1])
            else:
                return None
        except Exception as e:
            return None

    def _compute_quick_ratio(self):
        try:
            if self.bal[10][0] == 'Total Current Assets' and self.bal[7][0] == 'Total Inventory' and self.bal[23][0] == 'Total Current Liabilities':
                return self._round_decimal((self.bal[10][1] - self.bal[7][1]) / self.bal[23][1])
            else:
                return None
        except Exception as e:
            return None

    def _compute_shareholders_equity(self):
        try:
            if self.bal[17][0] == 'Total Assets' and self.bal[31][0] == 'Total Liabilities':
                return self._round_decimal(self.bal[17][1] - self.bal[31][1])
            else:
                return None
        except Exception as e:
            return None

    def _compute_return_on_equity(self):
        try:
            if self.inc[25][0] == 'Net Income':
                return self._round_decimal(self.inc[25][1] - self._compute_shareholders_equity())
            else:
                return None
        except Exception as e:
            return None

    def _compute_debt_equity_ratio(self):
        try:
            if self.bal[31][0] == 'Total Liabilities':
                return self._round_decimal(self.bal[31][1] / self._compute_shareholders_equity())
            else:
                return None
        except Exception as e:
            return None

    def _compute_net_profit_margin(self):
        try:
            if self.inc[25][0] == 'Net Income' and self.inc[3][0] == 'Total Revenue':
                return self._round_decimal(self.inc[25][1] / self.inc[3][1])
            else:
                return None
        except Exception as e:
            return None

    def _compute_free_cash_flow(self):
        try:
            if self.cas[7][0] == 'Cash from Operating Activities' and self.cas[8][0] == 'Capital Expenditures':
                return self._round_decimal(self.cas[7][1] + self.cas[8][1])
            else:
                return None
        except Exception as e:
            return None

    def _get_price_to_earnings_ratio(self):
        try:
            if self.data['price_to_earnings']:
                return self.data['price_to_earnings']
            else:
                return None
        except Exception as e:
            return None           
