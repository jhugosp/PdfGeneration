from infrastructure.entrypoint_execution.execution_handler import ExecutionHandler
from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.data_manager import DataManager
from application.data_handler.dto_generator import DtoGenerator
from domain.use_cases.entity_generation import EntityGenerator

from flask import render_template, Flask
import jinja2

app = Flask(__name__)
dto_generator = DtoGenerator(EntityGenerator())
image_manipulator = ImageManipulator()


@app.get("/")
def return_basic_html():
    dto = dto_generator.generate_dto()
    template_loader = jinja2.FileSystemLoader(searchpath="templates/")
    template_env = jinja2.Environment(loader=template_loader)
    template = template_env.get_template("sample_bancolombia.html")

    return render_template(template,
                           account_state=dto.account_state,
                           table_rows=dto.rows,
                           summary=dto.summary)


def main():
    execution_handler = ExecutionHandler(ImageManipulator(), dto_generator, DataManager())
    args = execution_handler.args

    if args.start_server:
        execution_handler.start_server()
    if args.quality_check:
        execution_handler.check_quality(args.quality_check)
    if args.image_enhancement:
        execution_handler.enhance_image(args.image_enhancement)
    if args.download_pdfs:
        execution_handler.file_download()
    if args.image_downgrade:
        execution_handler.downgrade_images()
    if args.generate_distorted_images:
        image_manipulator.generate_distorted_images()
    if args.generate_perfect_images:
        image_manipulator.save_perfect_images()
    if args.download_image_format:
        execution_handler.download_different_types_of_images()

    if not any(vars(args).values()):
        execution_handler.menu_printing()


if __name__ == "__main__":
    main()
