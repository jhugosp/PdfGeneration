from application.data_handler.data_manager import DataManager
from infrastructure.entrypoint_execution.execution_handler import ExecutionHandler
from application.image_manipulation.image_manipulator import ImageManipulator

from flask import Flask
from flask import render_template
import jinja2
import asyncio

from infrastructure.file_management.file_manager import download_pdfs

app = Flask(__name__)
image_manipulator = ImageManipulator()
data_manager = DataManager()


@app.get("/")
def return_basic_html():
    rows, summary, account_state = data_manager.prepare_pdf_information()
    data_manager.save_json_data(account_state_result=account_state, table_rows=rows, summary=summary)

    template_loader = jinja2.FileSystemLoader(searchpath="static/templates/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("sample_bancolombia.html")

    return render_template(template,
                           account_state=account_state,
                           table_rows=rows,
                           summary=summary)


async def main():
    execution_handler = ExecutionHandler(ImageManipulator())
    args = execution_handler.args

    if args.start_server:
        execution_handler.start_server()
    if args.quality_check:
        execution_handler.check_quality(args.quality_check)
    if args.image_enhancement:
        execution_handler.enhance_image(args.image_enhancement)
    if args.download_pdfs:
        await download_pdfs()
    if args.image_downgrade:
        execution_handler.downgrade_images()
    if args.generate_distorted_images:
        image_manipulator.generate_distorted_images()
    if args.generate_perfect_images:
        image_manipulator.save_perfect_images()

    if not any(vars(args).values()):
        execution_handler.menu_printing()

if __name__ == "__main__":
    asyncio.run(main())
