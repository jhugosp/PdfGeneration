from jinja2 import Environment, FileSystemLoader
from templates.bancolombia_model import Bancolombia
from constants.index import description_transactions
import pdfkit
import random
import datetime
import json
model_templates = Bancolombia()


def create_dates(transactions_amount):
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


def unify_results(dates, descriptions, branches, balances, transactions_values, transactions_amount):
    table_rows: list = []
    for _ in range(transactions_amount):
        row_template: dict = model_templates.row_template()
        row_template['date'] = dates[_]
        row_template['description'] = descriptions[_]
        row_template['branch'] = branches[_]
        row_template['dcto'] = 0.00
        row_template['charge_amount'] = transactions_values[_]
        row_template['present_balance'] = balances[_]

        table_rows.append(row_template)

    return table_rows


def create_summary(balances, transactions_values, transactions_amount, first_balance):
    total_balance = float(balances[len(balances) - 1].replace(',', ''))
    total_additions = 0
    total_subtractions = 0

    for value in transactions_values:
        float_value = float(value.replace(',', ''))

        if float_value < 0:
            total_subtractions += float_value
        else:
            total_additions += float_value

    summary_template = model_templates.summary_template()

    total_subtractions *= (-1)

    summary_template['previous_balance'] = first_balance
    summary_template['total_additions'] = f"{total_additions:,.2f}"
    summary_template['total_subtractions'] = f"{total_subtractions:,.2f}"
    summary_template['average_balance'] = f"{(total_balance / transactions_amount):,.2f}"
    summary_template['total_balance'] = f"{total_balance:,.2f}"

    return summary_template


def create_account_state():
    account_state = model_templates.account_state_template()
    account_state['account_number'] = str(random.randint(1000000000, 99999999999))

    return account_state


def write_results_to_file(account_state_result, table_rows, summary, file_name):
    file_loader = FileSystemLoader('static')
    env = Environment(loader=file_loader)
    template_out = env.get_template('sample_bancolombia.html')
    output = template_out.render(account_state=account_state_result, table_rows=table_rows, summary=summary)

    with open('static/result.html', 'w') as f:
        f.write(output)

    try:
        pdfkit.from_file(input="static/result.html", output_path=f'generated_pdfs/{file_name}.pdf')
    except OSError as e:
        print(f"Encountered issues when processing images: {str(e)}")
        pass
    finally:
        with open(f'pdfs_data/{file_name}.json', 'w') as f:
            json_data: dict = {
                "summary": summary,
                "table_rows": table_rows,
                "account_state": account_state_result
            }
            f.write(json.dumps(json_data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))

    print(f"{file_name} generated successfully!")


if __name__ == "__main__":
    initial_balance = model_templates.summary_template().get("previous_balance")
    for _ in range(random.randint(5, 10)):
        transactions = random.randint(5, 10)
        result_dates = create_dates(transactions)
        result_descriptions = create_descriptions(transactions)
        result_branches = create_branches(transactions)
        result_balances, result_transactions_values = calculate_balance(transactions, initial_balance)

        final_template_rows = unify_results(
            result_dates,
            result_descriptions,
            result_branches,
            result_balances,
            result_transactions_values,
            transactions)

        final_summary = create_summary(result_balances, result_transactions_values, transactions, initial_balance)

        final_account_state = create_account_state()

        write_results_to_file(
            account_state_result=final_account_state,
            table_rows=final_template_rows,
            summary=final_summary,
            file_name=f"report_{_ + 1}"
        )
