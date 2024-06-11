from application.dto.bancolombia_dto import BancolombiaDto
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

    output_dir = "application/data_generation/synthetic_pdfs"
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
                             output_dir)
            break
        else:
            print("Please enter correct input\n")
            continue


def generate_pdf(generator, css_path, background_image_path, gif_path, banner_path, output_dir):
    dto: BancolombiaDto = generator.generate_dto()

    html_content = generate_html(rows=dto.rows,
                                 summary=dto.summary,
                                 account_state=dto.account_state,
                                 css_path=css_path,
                                 background_image_path=background_image_path,
                                 gif_path=gif_path,
                                 banner_path=banner_path)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name, index = get_last_file_name(output_dir)
    html_file_path = os.path.join(output_dir, f"{file_name}.html")

    write_html_to_file(html_content, html_file_path)
    save_pdf_from_html_file(html_file_path, os.path.join(output_dir, f"{file_name}.pdf"))


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

        :param html_file_path:  Path to the HTML file.
        :param pdf_file_path:   Path to save the output PDF file.
    """
    options = {'enable-local-file-access': ''}
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
