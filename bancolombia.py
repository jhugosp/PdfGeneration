from jinja2 import Environment, FileSystemLoader
from templates.bancolombia_model import Bancolombia
import random
import datetime
from constants.index import description_transactions


model_templates = Bancolombia()


def give_date(transactions_amount):
    """Returns a deposit date randomly based on an amount of dates to give

        transactions_amount: Amount of dates to be generated based on the transactions to generate.
    :return: sorted list of dates
    """
    dates = []

    start_date = datetime.date(2023, 1, 1)
    end_date = datetime.date(2024, 1, 31)
    for _ in range(transactions_amount):
        random_date = start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))
        dates.append(random_date)

    dates.sort()

    return [date.strftime("%d/%m") for date in dates]


def create_descriptions(transactions_amount):
    descriptions = []
    for _ in range(transactions_amount):
        descriptions.append(random.choice(description_transactions))

    return descriptions


def create_branches(transaction_amount):
    branches = []
    branch_template: list = model_templates.branches_templates()
    for _ in range(transaction_amount):
        branches.append(random.choice(branch_template))

    return branches


def calculate_balance(transactions_amount: int, initial_balance: float) -> tuple:
    present_balances = []
    values_transactions = []
    previous_balance = initial_balance

    min_value = 0.01
    max_value = 9_999_999.99

    for _ in range(transactions_amount):
        possibility = random.random()
        random_number = random.uniform(min_value, max_value)

        if possibility < 0.5:
            if random_number > previous_balance:
                new_value = random.uniform(min_value, previous_balance) * (-1)
                previous_balance += new_value
                values_transactions.append(f"{new_value:,.2f}")
            else:
                random_number *= (-1)
                previous_balance += random_number
                values_transactions.append(f"{random_number:,.2f}")

        else:
            previous_balance += random_number
            values_transactions.append(f"{random_number:,.2f}")

        present_balances.append(f"{previous_balance:,.2f}")

    return present_balances, values_transactions


def write_results_to_file(template_out):
    output = template_out.render()

    with open('static/result.html', 'w') as f:
        f.write(output)
    print("HTML file generated successfully!")


account_state = model_templates.account_state_template()
summary = model_templates.summary_template()
table_rows = [
    model_templates.row_template()
]

if __name__ == "__main__":
    file_loader = FileSystemLoader('static')
    env = Environment(loader=file_loader)
    template = env.get_template('sample_banco_bogota.html')
    transactions = 10


    # write_results_to_file(template_out=template)
