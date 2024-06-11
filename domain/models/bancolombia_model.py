import datetime
import random


class Bancolombia:

    def __init__(self):
        self.rows, self.summary, self.account_state = self.initialize_bancolombia()

    def initialize_bancolombia(self) -> tuple:
        """ PDF information preparation function, in charge of generating:

            - Dates
            - Branches
            - Balances and transactions operations
            - Interest calculation
            - Total transactions
            - Operations summary
            - Account state formation

            :return: A tuple containing the final rows, summary and account state to present to client.
        """
        initial_balance = self.summary_template().get("previous_balance")
        transactions = random.randint(5, 10)

        dates = self.create_dates(transactions)

        branches = self.create_branches(transactions)

        balances, transactions_values, descriptions = (
            self.calculate_balance(transactions, initial_balance))

        final_template_rows, total_interest = self.aggregate_rows_information(
            dates=dates,
            descriptions=descriptions,
            branches=branches,
            balances=balances,
            transactions_values=transactions_values,
            transactions_amount=transactions,
        )

        final_summary = self.create_summary(
            balances=balances,
            transactions_values=transactions_values,
            transactions_amount=transactions,
            first_balance=initial_balance,
            interests=total_interest)

        final_account_state = self.create_account_state()

        return final_template_rows, final_summary, final_account_state

    @staticmethod
    def account_state_template() -> dict:
        """ Single registry that populates extract bounds information. (Bancolombia)

                from_date:          Initial date which takes tracking of transactions. (YYYY/MM/dd)
                until_date:         Final date which bound tracking of transactions. (YYYY/MM/dd)
                account_number:     Number of the account (9 - 11 length) Need to randomly generate.
                branch:             Branch in which the registry was generated.

                :returns:           Dict with a basic account state template
        """
        return {
            'from_date': '2023/12/31',
            'until_date': '2024/03/31',
            'account_number': '',
            'branch': 'SUCURSAL GIRÓN',
        }

    @staticmethod
    def summary_template() -> dict:
        """ Elements to populate summary (Banco de Bogotá)

            previous_balance:   Initial balance held in account
            total_additions:    Total of transactions which added to initial balance held in account.
            total_subtractions: Total of deductions which subtracted to initial balance held in account.
                                Calculate as a deduction/negative value. Paint as so
            average_balance:    Tax applied to each transaction. Investigate if it should be calculated as negative
                                value.
            accounts_demand:    4*1000 bank rule. Calculate as a deduction/negative value. Paint as so
            interests_payed:    Investigate what this field does, how does it affect calculations.
            source_retention:   Investigate what this field does, how does it affect calculations.
            total_balance:    This field is to be calculated and appended outside declaration as a last field

            :returns:           Dict with a basic summary template
        """
        return {
            'previous_balance': 100.00,
            'total_additions': 0.00,
            'total_subtractions': 0.00,
            'average_balance': 0.00,
            'accounts_demand': 0.00,
            'interests_payed': 0.00,
            'source_retention': 0.00,
            'total_balance': 0.00
        }

    @staticmethod
    def row_template() -> dict:
        """ Rows to populate extracts table (Banco de Bogotá)

            date:               Date the transaction took place (MM/dd format)
            cod_trans:          Transaction code (0000 length)
            description:        Description of transactions mentions place of transaction as well as card number.
            city:               City transaction took place (?)
            office_channel:     Office/channel in which transaction took place.
            dcto:               Discount of transaction.
            charge_amount:      Charge of transaction. Calculate as a deduction/negative value. Paint as so.
                                Needs to be in accordance with total_subtractions field in elements array.
            balance:            Present balance held in account. Initial value comes from elements.initial_balance and
                                present value needs to be calculated as balance -= charge_amount

                                Should also be used to update elements. total

            :returns:           Dict with a basic row template
        """
        return {
            'date': '',
            'description': '',
            'branch': '',
            'dcto': '',
            'charge_amount': 0.00,
            'present_balance': 0.00
        }

    @staticmethod
    def create_branches(transaction_amount):
        """ Generated a list containing random branches from a bank.

            :param transaction_amount:  Amount of transactions performed which require an equal amount of branches.
            :return:                    List of branches.
        """
        branches = []
        branch_template: list = Bancolombia.branches_templates()
        for _ in range(transaction_amount):
            branches.append(random.choice(branch_template))

        return branches

    @staticmethod
    def create_descriptions(transactions_amount):
        """ Generated a list containing random branches from a bank.

            :param transactions_amount:     Amount of transactions performed which require an equal amount of
                                            descriptions.
            :return:                        List of descriptions.
        """
        descriptions = []
        for _ in range(transactions_amount):
            descriptions.append(random.choice(Bancolombia.descriptions_templates()))

        return descriptions

    @staticmethod
    def create_dates(transactions_amount):
        """Returns a deposit date randomly based on an amount of dates to give

            :param transactions_amount:     Amount of dates to be generated based on the transactions to generate.
            :return:                        Sorted list of dates
        """
        dates = []

        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2024, 1, 31)
        for _ in range(transactions_amount):
            random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
            dates.append(random_date)

        dates.sort()

        return [date.strftime("%d/%m") for date in dates]

    @staticmethod
    def calculate_balance(transactions_amount: int, initial_balance: float) -> tuple:
        """ Transactions operating in order to calculate balance coming from user perceived operations.

            The function is in charge of calculating the present balance held in an account, if there is a charge or
            a deposit made and if so, validate if there is an interest to be taken into account.

            To differentiate between charges, deposits and interest calculation, simple if statements validate the
            chance of an option by generating a random number. Likewise, the amount of a transaction is a randomized
            value and is subject to change when an initially proposed charge is greater than the money initially held
            in an account.

            :param transactions_amount:     Amount of transactions to be processed for a user.
            :param initial_balance:         Initial balance held in an account before performing calculations.
            :return:
        """
        present_balances = []
        values_transactions = []
        descriptions = []
        previous_balance = initial_balance

        min_value = 0.01
        max_value = 9_999_999.99

        for _ in range(transactions_amount):
            possibility = random.random()
            random_number = random.uniform(min_value, max_value)
            description = random.choice(Bancolombia.descriptions_templates())

            if possibility < 0.5:
                while True:
                    description = random.choice(Bancolombia.descriptions_templates())
                    if "INTERESES" not in description:
                        if random_number > previous_balance:
                            new_value = random.uniform(min_value, previous_balance) * (-1)
                            previous_balance += new_value
                            values_transactions.append(f"{new_value:,.2f}")
                        else:
                            random_number *= (-1)
                            previous_balance += random_number
                            values_transactions.append(f"{random_number:,.2f}")
                        break
                    else:
                        continue

            else:
                previous_balance += random_number
                values_transactions.append(f"{random_number:,.2f}")

            descriptions.append(description)
            present_balances.append(f"{previous_balance:,.2f}")

        return present_balances, values_transactions, descriptions

    @staticmethod
    def aggregate_rows_information(**kwargs):
        """ Aggregation of results coming from the PDF information preparation function in regard to row templating
            and interest calculation.

            :param kwargs:      Parameters received by function which, in essence, are:

                                - dates:                List of dates to be related to a transaction
                                - descriptions:         Description held by a transaction
                                - branches:             List of branches to be chosen from, to relate to a transaction
                                - transactions_values:  List of charges and deposits made from a user.
                                - transactions_amount:  Amount of transactions performed by a user.
            :return:            A tuple containing the unified information as dict list of table rows, and the total
                                interest accrued by a user
        """
        dates = kwargs.get('dates')
        descriptions = kwargs.get('descriptions')
        branches = kwargs.get('branches')
        balances = kwargs.get('balances')
        transactions_values = kwargs.get('transactions_values')
        transactions_amount = kwargs.get('transactions_amount')

        total_interest = 0
        table_rows: list = []
        for _ in range(transactions_amount):
            if "INTERESES" in descriptions[_]:
                total_interest += float(transactions_values[_].replace(',', ''))

            row_template: dict = Bancolombia.row_template()
            row_template['date'] = dates[_]
            row_template['description'] = descriptions[_]
            row_template['branch'] = branches[_]
            row_template['dcto'] = 0.00
            row_template['charge_amount'] = transactions_values[_]
            row_template['present_balance'] = balances[_]

            table_rows.append(row_template)

        return table_rows, total_interest

    @staticmethod
    def create_summary(**kwargs):
        """ Final summarization of balance, charges and deposits in a user bank extract.

            The function transforms and calculates the sequential previous balance, total of deposits, interest and
            charges as well as the total and average balance in the user account

            :param kwargs:      Parameters received by function which, in essence, are:

                                - balances:             List of dates to be related to a transaction
                                - transactions_values:  List of charges and deposits made from a user.
                                - transactions_amount:  Amount of transactions performed by a user.
                                - first_balance:        First balance held in account by a user.
                                - interests:            List of interests values accrued by a user.
            :return:            A dict containing the replaced information.
        """
        balances = kwargs.get('balances')
        transactions_values = kwargs.get('transactions_values')
        transactions_amount = kwargs.get('transactions_amount')
        first_balance = kwargs.get('first_balance')
        interests = kwargs.get('interests')

        total_balance = float(balances[len(balances) - 1].replace(',', ''))
        total_additions = 0
        total_subtractions = 0

        for value in transactions_values:
            float_value = float(value.replace(',', ''))

            if float_value < 0:
                total_subtractions += float_value
            else:
                total_additions += float_value

        summary_template = Bancolombia.summary_template()

        total_subtractions *= (-1)

        summary_template['previous_balance'] = first_balance
        summary_template['total_additions'] = f"{total_additions:,.2f}"
        summary_template['total_subtractions'] = f"{total_subtractions:,.2f}"
        summary_template['average_balance'] = f"{(total_balance / transactions_amount):,.2f}"
        summary_template['total_balance'] = f"{total_balance:,.2f}"
        summary_template['interests_payed'] = f"{interests:,.2f}"

        return summary_template

    @staticmethod
    def create_account_state():
        """ Creates a basic account state with an initialized random account number.

            :return:    dict which represents a basic account_state object.
        """
        account_state = Bancolombia.account_state_template()
        account_state['account_number'] = str(random.randint(100000000, 99999999999))

        return account_state

    @staticmethod
    def branches_templates():
        """ Returns a simple list of default values for branches

            :return: list of strings comprised of cities' names
        """
        return ["GIRÓN", "BOGOTÁ", "CORRESPONSA", "MEDELLÍN", "CALI", "PASTO", "BOYACÁ"]

    @staticmethod
    def descriptions_templates():
        """ Returns a simple list of default values for descriptions

            :return: list of strings comprised of cities' names
        """
        return [
            "ABONO INTERESES A LA CUENTA 654****1234 DE AHORROS PERSONAS BANCOLOMBIA. PAGO MÍNIMO REALIZADO EN PESOS "
            "COLOMBIANOS",
            "PAGO PSE BANCO DAVIVIENDA SA CON TARJETA 123****891 Y CHEQUERA VIRTUAL PSE",
            "ABONO INTERESES AHORROS",
            "CUOTA INTERESES TARJETA DEBITO",
            "PAGO INTERBANC WIZELINE SAS",
            "TRANSFERENCIA CTA SUC VIRTUAL",
            "PAGO SUC VIRT TC VISA MEDIANTE UN CHEQUE DIRECTAMENTE EN SUCURSAL FÍSICA BANCOLOMBIA. PAGO REALIZADO EN "
            "DÓLARES",
            "PAGO PSE P.A. ADDI",
            "PAGO PSE Portal Zona Pagos BB",
            "PAGO INTERESES NU COLOMBIA SA",
            "PAGO PSE Acueducto Metropolit",
            "PAGO SUC VIRT TC AMEX PESOS",
            "PAGO SUC VIRT TC AMEX DOLAR",
            "TRANSFERENCIA CTA SUC VIRTUAL MEDIANTE TARJETA 875****1234 DE CRÉDITO BANCOLOMBIA. PAGO REALIZADO CON LA "
            "TARJETA 9191****212 VISA MASTERCARD"
        ]
