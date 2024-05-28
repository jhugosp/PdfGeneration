from jinja2 import Environment, FileSystemLoader
from templates.bancolombia_model import account_state_template, summary_template, row_template
import random
import datetime


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
        descriptions.append(f"Description_{_}")

    return descriptions


def write_results_to_file(template_out):
    output = template_out.render()

    with open('static/result.html', 'w') as f:
        f.write(output)
    print("HTML file generated successfully!")


account_state = account_state_template()

summary = summary_template()

table_rows = [
    row_template()
]


if __name__ == "__main__":
    file_loader = FileSystemLoader('static')
    env = Environment(loader=file_loader)
    template = env.get_template('sample_banco_bogota.html')

    print(f"dates is: {give_date(10)}")

    # write_results_to_file(template_out=template)
