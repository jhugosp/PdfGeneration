import argparse

from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.dto_generator import DtoGenerator
from application.data_handler.data_manager import DataManager
from infrastructure.file_management.file_manager import download_pdf
from domain.models.enhancers.opencv_enhancer import OpencvEnhancer
from domain.models.enhancers.pillow_enhancer import PillowEnhancer
import os
import random
import subprocess

from domain.models.converter.pdf_to_jpg import PDFToJPGConverter
from domain.models.converter.pdf_to_png import PDFToPNGConverter
from domain.models.converter.pdf_to_jpeg import PDFToJPEGConverter
from domain.models.converter.pdf_to_tiff import PDFToTIFFConverter

from domain.models.converter.file_to_png import FileToPNGConverter


class ExecutionHandler:

    def __init__(self, image_manipulator: ImageManipulator, dto_generator: DtoGenerator, data_manager: DataManager):
        self.dto_generator = dto_generator
        self.data_manager = data_manager
        self._args = self.prepare_args_parser()
        self._image_manipulator = image_manipulator

    @property
    def args(self):
        return self._args

    def menu_printing(self):
        while True:
            option = input("""\nPlease enter what you want to do:
1. Check quality of a given image.
2. Enhance quality of given image.
3. Download x amount of PDF files from live server.
4. Downgrade Image quality of a directory of perfect png images and generate PDFs.
5. Generate distorted png images from a directory containing distorted PDFs.
6. Generate perfect images from files stored from live server.
7. Download different type of images (PNG, JPG, JPEG, etc) 
8. Download PNG to different type file (PDF, JPG, JPEG)
Press anything else to quit.\n""")

            match option:

                case "1":
                    # Example image_path: application/data_generation/generated_images/real_case/extract_1_1.png
                    image_path = input("Enter path to check image quality: ")
                    self.check_quality(image_path)
                    continue
                case "2":
                    # Example image_path: application/data_generation/generated_images/real_case/extract_1_1.png
                    image_path = input("Enter path to check image quality: ")
                    self.enhance_image(image_path)
                    continue
                case "3":
                    try:
                        self.file_download()
                    except Exception as ex:
                        print(f"Something went wrong: {ex}")
                    finally:
                        continue
                case "4":
                    self.downgrade_images()
                    continue
                case "5":
                    self._image_manipulator.generate_distorted_images()
                    continue
                case "6":
                    self._image_manipulator.save_perfect_images()
                    continue
                case "7":
                    self.download_different_types_of_images()
                    continue
                case "8":
                    self.convert_file_to_png()
                    continue
                case _:
                    break

    @staticmethod
    def prepare_args_parser():
        args_parser = argparse.ArgumentParser(
            description="Script that performs image enhancement/downgrade/transformation or PDF handling and download. "
        )

        args_parser.add_argument("--start-server",
                                 required=False,
                                 default=False,
                                 action='store_true',
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
                            application/data_generation/generated_images/real_case/extract_1_1.png
                    
                            Stores enhanced images under: 
                            application/data_generation/generated_images/image_enhancement/**""")
        args_parser.add_argument("--image-downgrade",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Downgrades a directory of perfect images and stores themas PDF files
                                   under application/data_generation/distorted_pdfs/**""")
        args_parser.add_argument("--download-pdfs",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Prompts N amount of PDF files to download from server and stores them
                                    under application/data_generation/synthetic_pdfs/**""")
        args_parser.add_argument("--generate-distorted-images",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Downloads png files extracted from PDFs which show distorted images and
                                    stores the under application/data_generation/generated_images/**""")
        args_parser.add_argument("--generate-perfect-images",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Downloads png files extracted from PDFs which show perfect images and stores
                                    them under application/data_generation/generated_images/perfect""")

        return args_parser.parse_args()

    def file_download(self):
        """ Execution of asynchronous browser PDF printing.

        :return:    Nothing.
        """
        try:
            download_pdf(dto_generator=self.dto_generator,
                         data_manager=self.data_manager,
                         css_path=os.path.abspath("static/assets/fuentes.css"),
                         background_image_path=os.path.abspath("static/assets/CtaCte_1_v1.png"),
                         gif_path=os.path.abspath("static/assets/pxlTransp.gif"),
                         banner_path=os.path.abspath("static/assets/IMG2024MAR_CH7258.jpeg"))
        except TypeError as e:
            print(f"Something went wrong while downloading files: {e}")

    @staticmethod
    def start_server():
        """ Simple command line script execution which starts Flask Server

        :return:    Nothing.
        """
        print("Starting the server...")
        try:
            subprocess.run(["flask", "--app", "bancolombia.py", "run", "--debug"], capture_output=True,
                           text=True,
                           check=True)
        except subprocess.CalledProcessError as e:
            if "Address already in use" in e.stderr:
                print("Server is already up")
            else:
                print(f"An error occurred while running the Flask app: {e.stderr}")

    def check_quality(self, quality_check):
        """ Checks image quality by printing blurriness, noise and sharpness.

        :param quality_check:   Path of the image to check the quality to.
        :return:                Tuple containing blurriness, noise and sharpness.
        """
        self._image_manipulator.assess_image_quality(quality_check)

    def enhance_image(self, image_enhancement):
        """ Enhances through user defined inputs, the amount of enhancements and the enhancer to use on an image.

            Enhancement stores result images on:

            application/data_generation/generated_images/image_enhancement/**

        :param image_enhancement:       Path of image to enhance quality to. Example:
                                        - application/data_generation/generated_images/distorted_1/extract_1_1.png
        :return:                        Nothing.
        """
        iterations = int(input("How many iterations would you go through? "))
        enhancer = input("Which enhancer do you want to use? (pillow, opencv)")
        for _ in range(iterations if 0 < iterations < 10 else 5):
            index = (_ + 1)
            while True:
                match enhancer:
                    case "pillow":
                        print(f"Pillow - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  PillowEnhancer())
                        break
                    case "opencv":
                        print(f"OpenCV - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  OpencvEnhancer())
                        break
                    case _:
                        print("Please enter a valid value.")
                        enhancer = input("Which enhancer do you want to use? (pillow, opencv)")
                        continue

    def downgrade_images(self):
        """ Performs image downgrading by applying one of two filters.

        :return:    Nothing.
        """
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

                distorted_image = self._image_manipulator.distort_image(input_image_path, distortion_type)
                self._image_manipulator.image_to_pdf(distorted_image, output_pdf_path)

                print(f"Distorted PDF saved to {output_pdf_path}")

    @staticmethod
    def download_different_types_of_images():
        image_type = input("""\nChoose the type of image to download:
        1. PNG
        2. TIFF
        3. JPG
        4. JPEG
        Press any other key to return to the main menu.\n""")

        converter_map = {
            "1": PDFToPNGConverter(),
            "2": PDFToTIFFConverter(),
            "3": PDFToJPGConverter(),
            "4": PDFToJPEGConverter()
        }

        output_folder_map = {
            "1": "PNG",
            "2": "TIFF",
            "3": "JPG",
            "4": "JPEG"
        }

        converter = converter_map.get(image_type)
        if converter:
            pdf_path = "application/data_generation/synthetic/pdf"
            base_output_folder = "application/data_generation/shyntetic_images"

            output_folder = os.path.join(base_output_folder, output_folder_map.get(image_type))

            converter.convert(pdf_path, output_folder)
            print(f"{image_type} images downloaded successfully.")
        else:
            print("Invalid option.")

    @staticmethod
    def convert_file_to_png():
        converter = FileToPNGConverter()

        if converter:
            pdf_path = "application/data_generation/files"
            base_output_folder = "application/data_generation/shyntetic_images/FILES"

            converter.convert(pdf_path, base_output_folder)
            print(f"files converted successfully.")
        else:
            print("Invalid option.")

