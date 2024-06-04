from jinja2 import Environment, FileSystemLoader
from models.bancolombia_model import Bancolombia, create_account_state, create_summary, create_branches
from models.bancolombia_model import create_dates, calculate_balance, unify_results
from image_transformation import pdf_to_png, list_files_in_directory, de_blur_image, assess_image_quality
from pyppeteer_download import save_page_as_pdf
from flask import Flask
from flask import render_template
import asyncio
import pdfkit
import random
import json

app = Flask(__name__)
model_templates = Bancolombia()


def return_html_string(account_state_result, table_rows, summary):
    file_loader = FileSystemLoader('static')
    env = Environment(loader=file_loader)
    template_out = env.get_template('sample_bancolombia.html')
    return template_out.render(account_state=account_state_result, table_rows=table_rows, summary=summary)


def write_results_to_file(account_state_result, table_rows, summary, file_name):
    output = return_html_string(account_state_result, table_rows, summary)

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


@app.get("/")
def return_basic_html():
    initial_balance = model_templates.summary_template().get("previous_balance")
    transactions = random.randint(5, 10)

    dates = create_dates(transactions)

    branches = create_branches(transactions)

    balances, transactions_values, descriptions = (
        calculate_balance(transactions, initial_balance))

    final_template_rows, total_interest = unify_results(
        dates=dates,
        descriptions=descriptions,
        branches=branches,
        balances=balances,
        transactions_values=transactions_values,
        transactions_amount=transactions,
    )

    final_summary = (create_summary(
        balances=balances,
        transactions_values=transactions_values,
        transactions_amount=transactions,
        first_balance=initial_balance,
        interests=total_interest)
    )

    final_account_state = create_account_state()

    return render_template('sample_bancolombia.html',
                           account_state=final_account_state,
                           table_rows=final_template_rows,
                           summary=final_summary)


async def download_pdfs() -> None:
    url = "http://localhost:5000/"
    output_dir = "pdfs_data"
    iterations = int(input("How many files will you download? "))

    await save_page_as_pdf(url, iterations, output_dir)
    await asyncio.get_event_loop().run_until_complete(save_page_as_pdf(url, iterations, output_dir))


def generate_distorted_images():
    consulted_dir = input("Which directory will you consult? (output-1/output-2) ")
    dir_path = f"images-distorted/{consulted_dir}"
    extracted_files: [] = list_files_in_directory(dir_path)
    for _ in range(len(extracted_files)):
        pdf_to_png(
            f'{dir_path}/{extracted_files[_]}',
            f'generated_images/real_case/',
            (_ + 1)
        )
    print(f"Successfully printed image: {_ + 1}")


if __name__ == "__main__":
    # generate_distorted_images()
    print("Real quality image:")
    assess_image_quality("generated_images/real_case/extract_1_1.png")
    img_path = "generated_images/test/extract_1_1.png"

    for _ in range(10):
        print(f"Image name: {img_path}")
        img_path = de_blur_image(img_path, _)
