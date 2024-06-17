from infrastructure.entrypoint_execution.execution_handler import ExecutionHandler
from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.data_manager import DataManager
from application.data_handler.dto_generator import DtoGenerator
from domain.use_cases.entity_generation import EntityGenerator

from flask import Flask

app = Flask(__name__)
#   TODO: generate controller to consult documents based on banks
dto_generator = DtoGenerator(EntityGenerator())
image_manipulator = ImageManipulator()


def main():
    execution_handler = ExecutionHandler(ImageManipulator(), dto_generator, DataManager())
    args = execution_handler.args

    if args.quality_check:
        execution_handler.check_quality(args.quality_check)
    if args.image_enhancement:
        execution_handler.enhance_image(args.image_enhancement)
    if args.download_pdfs:
        execution_handler.file_download()
    if args.download_png_files:
        execution_handler.convert_file_to_png()

    if not any(vars(args).values()):
        execution_handler.menu_printing()


if __name__ == "__main__":
    main()
