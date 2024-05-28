from jinja2 import Environment, FileSystemLoader
from templates.bancolombia_model import account_state_template, summary_template, row_template
import datetime


def give_date(year, month, day) -> datetime.date:
    return datetime.date(year=year, month=month, day=day)


file_loader = FileSystemLoader('static')
env = Environment(loader=file_loader)
template = env.get_template('sample_banco_bogota.html')

account_state = account_state_template()

summary = summary_template()

table_rows = [
    row_template()
]

output = template.render()

with open('static/result.html', 'w') as f:
    f.write(output)

print("HTML file generated successfully!")
