def account_state_template() -> dict:
    """ Single registry that populates extract bounds information. (Bancolombia)

            from_date:          Initial date which takes tracking of transactions. (YYYY/MM/dd)
            until_date:         Final date which bound tracking of transactions. (YYYY/MM/dd)
            account_number:     Number of the account (9 - 11 length) Need to randomly generate.
            branch:             Branch in which the registry was generated.
    """
    return {
        'from_date': '2023/12/31',
        'until_date': '2024/03/31',
        'account_number': '123456789',
        'branch': 'SUCURSAL GIRÓN',
    }


def summary_template() -> dict:
    """Elements to populate summary (Banco de Bogotá)

            previous_balance:   Initial balance held in account
            total_additions:    Total of transactions which added to initial balance held in account.
            total_subtractions: Total of deductions which subtracted to initial balance held in account.
                                Calculate as a deduction/negative value. Paint as so
            average_balance:    Tax applied to each transaction. Investigate if it should be calculated as negative
                                value.
            accounts_demand:    4*1000 bank rule. Calculate as a deduction/negative value. Paint as so
            interests_payed:    Investigate what this field does, how does it affect calculations.
            source_retention:   Investigate what this field does, how does it affect calculations.
            present_balance:    This field is to be calculated and appended outside declaration as a last field
    """
    return {
        'previous_balance': 100.00,
        'total_additions': 0.00,
        'total_subtractions': 0.00,
        'average_balance': 0.00,
        'accounts_demand': 0.00,
        'interests_payed': 0.00,
        'source_retention': 0.00,
        'present_balance': 0.00
    }


def row_template() -> dict:
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
    return {
        'date': '',
        'description': '',
        'branch': '',
        'document': '',
        'charge_amount': 0.00,
        'present_balance': 0.00
    }
