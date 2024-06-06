import random

from application.image_manipulation.image_transformation import ImageManipulator
from application.data_handler.data_manager import DataManager

from flask import Flask
from flask import render_template
import jinja2
import asyncio
import os
import argparse
import subprocess

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


def menu_printing():
    while True:
        option = input("""\nPlease enter what you want to do:
1. Check quality of a given image.
2. Enhance quality of given image.
3. Download x amount of PDF files from live server.
4. Downgrade Image quality of a directory of perfect png images and generate PDFs.
5. Generate distorted png images from a directory containing distorted PDFs.
6. Generate perfect images from files stored from live server.
            
Press anything else to quit.\n""")

        match option:

            case "1":
                # Example image_path: application/data_generation/generated_images/real_case/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                check_quality(image_path)
                continue
            case "2":
                # Example image_path: application/data_generation/generated_images/real_case/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                enhance_image(image_path)
                continue
            case "3":
                try:
                    file_download()
                except Exception as ex:
                    print(f"Something went wrong: {ex}")
                finally:
                    continue
            case "4":
                downgrade_images()
                continue
            case "5":
                image_manipulator.generate_distorted_images()
                continue
            case "6":
                image_manipulator.save_perfect_images()
                continue
            case _:
                break


def file_download():
    try:
        asyncio.run(download_pdfs())
    except RuntimeError:
        print("Finished PDF saving.")


def check_quality(quality_check):
    image_manipulator.assess_image_quality(quality_check)


def enhance_image(image_enhancement):
    # Example image_path: application/data_generation/generated_images/distorted_2/extract_1_1.png
    iterations = int(input("How many iterations would you go through? "))
    for _ in range(iterations if 0 < iterations < 10 else 5):
        print(f"Image name: {image_enhancement}")
        image_enhancement = image_manipulator.de_blur_image(image_enhancement, (_ + 1))


def downgrade_images():
    input_directory = 'application/data_generation/generated_images/perfect'
    for filename in os.listdir(input_directory):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            distortion_type = 0.5 < random.random()
            input_image_path = os.path.join(input_directory, filename)

            if distortion_type:
                output_directory = "application/data_generation/distorted_pdfs/distorted_1/"
            else:
                output_directory = "application/data_generation/distorted_pdfs/distorted_2/"

            output_pdf_path = (
                os.path.join(output_directory, os.path.splitext(filename)[0] + '_distorted.pdf'))

            distorted_image = image_manipulator.distort_image(input_image_path, distortion_type)
            image_manipulator.image_to_pdf(distorted_image, output_pdf_path)

            print(f"Distorted PDF saved to {output_pdf_path}")


def prepare_args_parser():
    args_parser = argparse.ArgumentParser(
        description="Script that performs image enhancement/downgrade/transformation or PDF handling and download. "
    )

    args_parser.add_argument("--start-server",
                             required=False,
                             default=False,
                             help="Simple instruction to boot live server.")
    args_parser.add_argument("--quality-check",
                             required=False,
                             type=str,
                             help="""Path of image to check quality to. 
                        Example:
                        application/data_generation/generated_images/real_case/extract_1_1.png
                        """)
    args_parser.add_argument("--image-enhancement",
                             required=False,
                             type=str,
                             help="""Path of image to enhance quality to.
                        Example:
                        application/data_generation/generated_images/real_case/extract_1_1.png""")
    args_parser.add_argument("--image-downgrade",
                             required=False,
                             default=False,
                             help="Downgrades a directory of perfect images and stores them in another location.")
    args_parser.add_argument("--download-pdfs",
                             required=False,
                             default=False,
                             help="Prompts N amount of PDF files to download from server.")
    args_parser.add_argument("--generate-distorted-images",
                             required=False,
                             default=False,
                             help="Downloads png files extracted from PDFs which show distorted images.")
    args_parser.add_argument("--generate-perfect-images",
                             required=False,
                             default=False,
                             help="Downloads png files extracted from PDFs which show perfect images.")

    return args_parser


if __name__ == "__main__":
    #   Command line menu args definitions:
    parser = prepare_args_parser()
    args = parser.parse_args()

    if args.start_server:
        print("Starting the server...")
        try:
            subprocess.run(["flask", "--app", "bancolombia.py", "run", "--debug"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running the Flask app: {e}")
    if args.quality_check:
        check_quality(args.quality_check)
    if args.image_enhancement:
        enhance_image(args.image_enhancement)
    if args.download_pdfs:
        asyncio.run(download_pdfs())
    if args.image_downgrade:
        downgrade_images()
    if args.generate_distorted_images:
        image_manipulator.generate_distorted_images()
    if args.generate_perfect_images:
        image_manipulator.save_perfect_images()

    # If no arguments were provided, show the menu
    if not any(vars(args).values()):
        menu_printing()
