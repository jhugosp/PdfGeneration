from jinja2 import Environment, FileSystemLoader
import datetime


def give_date(year, month, day) -> datetime.date:
    return datetime.date(year=year, month=month, day=day)


file_loader = FileSystemLoader('static')
env = Environment(loader=file_loader)
template = env.get_template('sample_banco_bogota.html')

bounds = [
    {
        """ Single registry that populates extract bounds information. (Banco de Bogotá)
            extract_date:       Period bound by from_date - until_date (from_date - until_date YYYY format)
            from_date:          Initial date which takes tracking of transactions. (Month_Name dd format)
            until_date:         Final date which bound tracking of transactions. (Month_Name dd format)
            account_number:     Number of the account (000000000 length)
            account_type:       Type of account: Cuentas Privadas - Cuentas Públicas
            origin_code:        Code of origin (0000 length)
            city:               City of registry (?)
        """
        'from_date': give_date(year=2023, month=1, day=1),
        'until_date': give_date(year=2024, month=1, day=31),
        'account_number': '123456789',
        'account_type': 'Cuentas Privadas',
        'origin_code': '0001',
        'city': 'BOGOTA'
    },
]

elements = [
    {
        """Elements to populate summary (Banco de Bogotá)
        
            initial_balance:    Initial balance held in account
            total_additions:    Total of transactions which added to initial balance held in account.
            total_subtractions: Total of deductions which subtracted to initial balance held in account. 
                                Calculate as a deduction/negative value. Paint as so
            iva_tax:            Tax applied to each transaction. Investigate if it should be calculated as negative 
                                value.
            gmf:                4*1000 bank rule. Calculate as a deduction/negative value. Paint as so
            retention:          Investigate what this field does, how does it affect calculations.
            interest:           Investigate what this field does, how does it affect calculations.
            total:              This field is to be calculated and appended outside declaration as a last field
        """
        'initial_balance': 44.44,
        'total_additions': 22.22,
        'total_subtractions': 10.22,
        'iva_tax': 0.00,
        'gmf': 6754.75,
        'retention': 0.00,
        'interest': 13.33,
        'total': 56.22
    }
]

table_rows = [
    {
        """Rows to populate extracts table (Banco de Bogotá)
        
        date:               Date the transaction took place (MM/dd format)
        cod_trans:          Transaction code (0000 length)
        description:        Description of transactions mentions place of transaction as well as card number.
        city:               City transaction took place (?)
        office_channel:     Office/channel in which transaction took place.
        document:           Document of transaction holder.
        charge_amount:      Charge of transaction. Calculate as a deduction/negative value. Paint as so. 
                            Needs to be in accordance with total_subtractions field in elements array.
        balance:            Present balance held in account. Initial value comes from elements.initial_balance and 
                            present value needs to be calculated as balance -= charge_amount
                 
                            Should also be used to update elements.total
        """
        
        'date': give_date(year=2023, month=10, day=12),
        'cod_trans': 0o012,
        'description': "Compra realizada el {} con tarjeta 12****54321",
        'city': 'Bogota',
        'office_channel': 'Calle 10',
        'document': '689123',
        'charge_amount': 2.10,
        'balance': 42.12
    },
]

output = template.render(elements=elements, bounds=bounds, rows=table_rows)

with open('static/result.html', 'w') as f:
    f.write(output)

print("HTML file generated successfully!")
