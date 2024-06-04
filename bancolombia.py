import random

from application.image_manipulation.image_transformation import ImageManipulator
from application.data_handler.data_manager import DataManager

from flask import Flask
from flask import render_template
import jinja2
import asyncio
import os

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


if __name__ == "__main__":
    while True:
        option = input("""\nPlease enter what you want to do:
1. Check quality of a given image.
2. Enhance quality of given image.
3. Download x amount of PDF files from live server.
4. Downgrade Image quality of a directory of perfect png images and generate PDFs.
5. Generate distorted png images from a directory containing distorted PDFs.
            
Press anything else to quit.\n""")

        match option:

            case "1":
                # Example image_path: application/data_generation/generated_images/real_case/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                image_manipulator.assess_image_quality(image_path)
                continue
            case "2":
                # Example image_path: application/data_generation/generated_images/distorted_2/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                iterations = int(input("How many iterations would you go through? "))
                for _ in range(iterations if 0 < iterations < 10 else 5):
                    print(f"Image name: {image_path}")
                    image_path = image_manipulator.de_blur_image(image_path, (_ + 1))
                continue
            case "3":
                try:
                    asyncio.run(download_pdfs())
                except RuntimeError as e:
                    print("Finished PDF saving.")
                finally:
                    continue
            case "4":
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
                continue
            case "5":
                image_manipulator.generate_distorted_images()
                continue
            case _:
                break
