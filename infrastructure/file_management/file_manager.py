from application.dto.bancolombia_dto import BancolombiaDto
from application.data_handler.data_manager import DataManager
import jinja2
import pdfkit
import os
import re


def download_pdf(**kwargs):
    """ Generates a PDF file from a Jinja2 template and data coming from a data generator.

        - Account state of account to save.
        - Summary of deposits, charges and interests.
        - Transaction information rows in table.
        - Directory to store the generated PDF file.
        - Absolute path to the CSS file.
        - Absolute path to the background image file.

        :return:   Path to the generated PDF file.
    """

    output_dir = "application/data_generation/synthetic"
    data_manager = kwargs.get('data_manager')
    css_path = kwargs.get('css_path')
    background_image_path = kwargs.get('background_image_path')
    gif_path = kwargs.get('gif_path')
    banner_path = kwargs.get('banner_path')

    while True:
        iterations = input("How many PDFs will you want? ")
        if iterations.isnumeric():
            for _ in range(int(iterations)):
                generate_pdf(kwargs.get('dto_generator'),
                             css_path,
                             background_image_path,
                             gif_path,
                             banner_path,
                             output_dir,
                             data_manager)
            break
        else:
            print("Please enter correct input\n")
            continue


def generate_pdf(generator, css_path, image_path, gif_path, banner_path, output_dir, data_manager: DataManager):
    dto: BancolombiaDto = generator.generate_dto()

    html_content = generate_html(rows=dto.rows,
                                 summary=dto.summary,
                                 account_state=dto.account_state,
                                 css_path=css_path,
                                 background_image_path=image_path,
                                 gif_path=gif_path,
                                 banner_path=banner_path)

    pdf_path, html_path = check_path_existence(output_dir)

    file_name, index = get_last_file_name(pdf_path)
    html_file_path = os.path.join(html_path, f"{file_name}.html")

    write_html_to_file(html_content, html_file_path)
    save_pdf_from_html_file(html_file_path, os.path.join(pdf_path, f"{file_name}.pdf"))

    data_manager.save_json_data(dto.account_state, dto.rows, dto.summary, file_name)


def check_path_existence(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pdf_path = f"{output_dir}/pdf"
    html_path = f"{output_dir}/html"

    if not os.path.exists(pdf_path):
        os.makedirs(pdf_path)

    if not os.path.exists(html_path):
        os.makedirs(html_path)

    return pdf_path, html_path


def generate_html(**kwargs):
    """ Generates HTML content from a Jinja2 template.

        :return: Rendered HTML content as a string.
    """

    rows = kwargs.get('rows')
    summary = kwargs.get('summary')
    account_state = kwargs.get('account_state')
    css_path = kwargs.get('css_path')
    background_image_path = kwargs.get('background_image_path')
    gif_path = kwargs.get('gif_path')
    banner_path = kwargs.get('banner_path')

    template_loader = jinja2.FileSystemLoader(searchpath="templates/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("sample_bancolombia_local.html")

    return template.render(account_state=account_state,
                           table_rows=rows,
                           summary=summary,
                           css_path=css_path,
                           background_image_path=background_image_path,
                           banner_path=banner_path,
                           gif_path=gif_path)


def write_html_to_file(html_content, output_file_path):
    """ Writes HTML content to an HTML file.

        :param html_content:        HTML content as a string.
        :param output_file_path:    Path to save the output HTML file.
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)


def save_pdf_from_html_file(html_file_path, pdf_file_path):
    """ Saves a PDF file from an HTML file using pdfkit.

        1 inch = 96 pixels
        1 inch = 25.4 mm
        1 pixel = 25.4 / 96 mm ≈ 0.264583 mm

        page_width_mm is the approximate conversion of px to mm: 776 pixels * 0.264583 mm/pixel ≈ 205.3 mm
        page_height_mm is the approximate conversion of px to mm: 1010 pixels * 0.264583 mm/pixel ≈ 267.8 mm

        The pixels used above are specified in the official HTML received from the bank.

        :param html_file_path:  Path to the HTML file.
        :param pdf_file_path:   Path to save the output PDF file.
    """
    page_width_mm = 205.3
    page_height_mm = 267.8

    options = {
        'enable-local-file-access': '',
        'no-pdf-compression': '',
        'disable-smart-shrinking': '',
        'page-width': f'{page_width_mm}mm',
        'page-height': f'{page_height_mm}mm',
        'margin-top': '0',
        'margin-right': '0',
        'margin-bottom': '0',
        'margin-left': '0',
    }
    pdfkit.from_file(html_file_path, pdf_file_path, options=options)


def get_last_file_name(directory) -> tuple[str, int]:
    highest_index = -1

    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_file():
                match = re.match(r"synthetic_(\d+)\.pdf", entry.name)
                if match:
                    index = int(match.group(1))
                    if index > highest_index:
                        highest_index = index

    new_index = highest_index + 1
    file_name = f"synthetic_{new_index}"
    print(f"Saving file: {file_name}")

    return file_name, new_index
