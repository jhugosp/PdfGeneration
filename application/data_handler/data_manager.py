from domain.models.bancolombia_model import Bancolombia
import json

model_templates = Bancolombia()


class DataManager:
    @staticmethod
    def save_json_data(account_state_result, table_rows, summary, file_name):
        """ Method which saves a json data or 'metadata' of an image.

            :param account_state_result:    Dictionary containing information about an account state to present to client.
            :param table_rows:              List of dictionaries containing information about the transactions of an extract
                                            to present to client.
            :param summary:                 Summary of transaction operations to present to client.
            :return:                        Nothing
        """
        try:
            with open(f'application/data_generation/pdfs_json_data/{file_name}.json', 'w') as f:
                json_data: dict = {
                    "summary": summary,
                    "table_rows": table_rows,
                    "account_state": account_state_result
                }
                f.write(json.dumps(json_data, indent=4, separators=(',', ': '), sort_keys=True, ensure_ascii=False))
        except IOError as e:
            print("Something went wrong: {}".format(str(e)))

