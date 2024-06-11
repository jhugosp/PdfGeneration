class BancolombiaDto:

    def __init__(self, rows, summary, account_state):
        self.rows = rows
        self.summary = summary
        self.account_state = account_state

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, value):
        self._rows = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    @property
    def account_state(self):
        return self._account_state

    @account_state.setter
    def account_state(self, value):
        self._account_state = value