import argparse

from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.dto_generator import DtoGenerator
from application.data_handler.data_manager import DataManager
from domain.models.enhancers.opencv_enhancer import OpencvEnhancer
from domain.models.enhancers.pillow_enhancer import PillowEnhancer

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
3. Consult dataset to get extracts.
4. Convert PNG to different type file (PDF, JPG, JPEG)
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
                    self.convert_file_to_png()
                    continue
                case _:
                    break

    @staticmethod
    def prepare_args_parser():
        args_parser = argparse.ArgumentParser(
            description="Script that performs image enhancement/downgrade/transformation or PDF handling and download. "
        )
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
        args_parser.add_argument("--consult-dataset",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Consults the dataset in order to obtain file/s to process""")
        args_parser.add_argument("--convert-png-files",
                                 required=False,
                                 default=False,
                                 action='store_true',
                                 help="""Downloads a PNG format specified by used based on existing different type of 
                                 files (PDF, JPG, JPEG)

                                    application/data_generation/shyntetic_images/FILES
                                 """)

        return args_parser.parse_args()

    def file_download(self):
        """ Execution of asynchronous browser PDF printing.

        :return:    Nothing.
        """
        try:
            #   TODO: Create recipe consult method
            print("Consult dataset")
        except TypeError as e:
            print(f"Something went wrong while downloading files: {e}")

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
        # TODO: Validate which kernel to use from the beginning
        iterations = int(input("How many iterations would you go through? "))
        enhancer = input("Which enhancer do you want to use? (pillow, opencv, both) ")
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
                    case "both":
                        print(f"Combined enhancing - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  PillowEnhancer(),
                                                                                  True)
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  OpencvEnhancer(),
                                                                                  True)
                        break
                    case _:
                        print("Please enter a valid value.")
                        enhancer = input("Which enhancer do you want to use? (pillow, opencv) ")
                        continue

    @staticmethod
    def convert_file_to_png():
        #   TODO: changed use of physical memory
        converter = FileToPNGConverter()

        if converter:
            pdf_path = "application/data_generation/files"
            base_output_folder = "application/data_generation/shyntetic_images/FILES"

            converter.convert(pdf_path, base_output_folder)
            print(f"files converted successfully.")
        else:
            print("Invalid option.")
