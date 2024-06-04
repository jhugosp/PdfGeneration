from application.image_manipulation.image_transformation import ImageManipulator
from application.data_handler.data_manager import DataManager

from flask import Flask
from flask import render_template
import jinja2

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
        option = int(input("""
            Please enter what you want to do:
            
            1. Check quality of a given image.
            2. Enhance quality of given image.
            3. Download x amount of PDF files from live server.
            4. Downgrade Image quality of a directory of images and generate PDFs.
            5. Generate distorted files from a directory containing PDFs.
            
            Press anything else to quit.
            
        """))

        match option:

            case 1:
                # Example: application/data_generation/generated_images/real_case/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                image_manipulator.assess_image_quality(image_path)
                continue
            case 2:
                # Example: application/data_generation/generated_images/real_case/extract_1_1.png
                image_path = input("Enter path to check image quality: ")
                for _ in range(10):
                    print(f"Image name: {image_path}")
                    img_path = image_manipulator.de_blur_image(image_path, _)
                continue
            case 3:
                continue
            case 4:
                continue
            case 5:
                continue
            case _:
                break

        # generate_distorted_images()

        # try:
        #     asyncio.run(download_pdfs())
        # except RuntimeError as e:
        #     print("Finished PDF saving.")
        # finally:
        #     sys.exit()

        # input_directory = 'static/input/'
        # output_directory = 'static/output/'

        # if not os.path.exists(output_directory):
        #     os.makedirs(output_directory)
        #
        # for filename in os.listdir(input_directory):
        #     if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
        #         input_image_path = os.path.join(input_directory, filename)
        #         output_pdf_path = os.path.join(output_directory, os.path.splitext(filename)[0] + '_distorted.pdf')
        #
        #         distorted_image = distort_image(input_image_path)
        #         image_to_pdf(distorted_image, output_pdf_path)
        #
        #         print(f"Distorted PDF saved to {output_pdf_path}")
