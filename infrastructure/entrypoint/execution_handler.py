import argparse

from application.image_manipulation.image_manipulator import ImageManipulator
from application.data_handler.dto_generator import DtoGenerator
from domain.models.enhancers.opencv_enhancer import OpencvEnhancer
from domain.models.enhancers.pillow_enhancer import PillowEnhancer

from domain.models.converter.file_to_png import FileToPNGConverter


class ExecutionHandler:

    def __init__(self, image_manipulator: ImageManipulator, dto_generator: DtoGenerator):
        self.dto_generator = dto_generator
        self._args = self.prepare_args_parser()
        self._image_manipulator = image_manipulator

    @property
    def args(self):
        return self._args

    @staticmethod
    def prepare_args_parser():
        args_parser = argparse.ArgumentParser(
            description="Script that performs image enhancement/transformation in multiple formats to PNG. ",
            formatter_class=argparse.RawTextHelpFormatter
        )
        args_parser.add_argument("-c", "--consult-dataset",
                                 required=True,
                                 type=int,
                                 nargs="+",
                                 help="""Consults the dataset in order to obtain file/s to process.
Receives document IDs (Integer value)""")
        args_parser.add_argument("-b", "--bank",
                                 required=True,
                                 help="""Indicates which Bank's document and rules are going to be worked on.
                                         
 Banks are: 
 
 - bancolombia 
 - banco-bogota 
 - bbva 
 - colpatria 
 - caja-social""")

        return args_parser.parse_args()

    @staticmethod
    def consult_dataset(document_id, bank, service):
        """ Execution of asynchronous browser PDF printing.

        :return:    Nothing.
        """
        try:
            #   TODO: Create recipe consult method
            result = None
            if len(document_id) == 1:
                result = service.get_one(document_id[0], bank)
                print(f"{result.code} - {result.metadata} - {result.rules} \nbank is: {bank}")
            elif len(document_id) > 1:
                result = service.get_multiple(document_id, bank)
                for index in result:
                    print(f"{index.code} - {index.metadata} - {index.rules} \nbank is: {bank}")

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
        # TODO: refactor implementation to obtain image differently than from path file. Validate how they come.
        iterations = int(input("How many iterations would you go through? "))
        enhancer = input("Which enhancer do you want to use? (pillow, opencv, both) ")
        kernel = input("Which kernel do you want to use? (simple, detailed)")
        for _ in range(iterations if 0 < iterations < 10 else 5):
            index = (_ + 1)
            while True:
                match enhancer:
                    case "pillow":
                        print(f"Pillow - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  PillowEnhancer(),
                                                                                  kernel)
                        break
                    case "opencv":
                        print(f"OpenCV - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  OpencvEnhancer(),
                                                                                  kernel)
                        break
                    case "both":
                        print(f"Combined enhancing - Image name: {image_enhancement}")
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  PillowEnhancer(),
                                                                                  kernel,
                                                                                  True)
                        image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                  index,
                                                                                  OpencvEnhancer(),
                                                                                  kernel,
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
