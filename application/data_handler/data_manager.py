from domain.models.bancolombia_model import Bancolombia
import uuid
import random
import json

model_templates = Bancolombia()


class DataManager:
    @staticmethod
    def save_json_data(account_state_result, table_rows, summary):
        """ Method which saves a json data or 'metadata' of an image.

            :param account_state_result:    Dictionary containing information about an account state to present to client.
            :param table_rows:              List of dictionaries containing information about the transactions of an extract
                                            to present to client.
            :param summary:                 Summary of transaction operations to present to client.
            :return:                        Nothing
        """
        try:
            with open(f'application/data_generation/pdfs_json_data/{uuid.uuid4().hex}.json', 'w') as f:
                json_data: dict = {
                    "summary": summary,
                    "table_rows": table_rows,
                    "account_state": account_state_result
                }
                f.write(json.dumps(json_data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))
        except IOError as e:
            print("Something went wrong: {}".format(str(e)))

    @staticmethod
    def prepare_pdf_information() -> tuple:
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
        initial_balance = model_templates.summary_template().get("previous_balance")
        transactions = random.randint(5, 10)

        dates = model_templates.create_dates(transactions)

        branches = model_templates.create_branches(transactions)

        balances, transactions_values, descriptions = (
            model_templates.calculate_balance(transactions, initial_balance))

        final_template_rows, total_interest = model_templates.aggregate_rows_information(
            dates=dates,
            descriptions=descriptions,
            branches=branches,
            balances=balances,
            transactions_values=transactions_values,
            transactions_amount=transactions,
        )

        final_summary = model_templates.create_summary(
            balances=balances,
            transactions_values=transactions_values,
            transactions_amount=transactions,
            first_balance=initial_balance,
            interests=total_interest)

        final_account_state = model_templates.create_account_state()

        return final_template_rows, final_summary, final_account_state
