import argparse
import random

from random import randrange
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

    def process_doc_data(self, bank, service):
        """ Execution of asynchronous browser PDF printing.

        :return:    Nothing.
        """
        try:
            #   TODO: Create recipe consult method, pass down
            result = None
            documents = self.give_documents_mock()
            if len(documents) == 1:
                result = service.get_one(documents[0].get("structured"),
                                         documents[0].get("raw"),
                                         documents[0].get("code"),
                                         documents[0].get("rules"),
                                         bank)
                print(f"Code: {result.code}  \nMetadata:{result.metadata} \nRules:{result.rules} \nbank is: {bank}")
            elif len(documents) > 1:
                result = service.get_multiple(documents, bank)
                for aux in result:
                    print(f"Code: {aux.code}  \nMetadata:{aux.metadata} \nRules:{aux.rules} \nbank is: {bank}")

        except TypeError as e:
            print(f"Something went wrong while downloading files: {e}")

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

        blurriness, noise, sharpness = self._image_manipulator.assess_image_quality(image=image_enhancement)

        # Define thresholds for what is considered a low quality image
        blurriness_threshold = 1000
        noise_threshold = 1e-10
        sharpness_threshold = 0.5
        if blurriness < blurriness_threshold or noise > noise_threshold or sharpness < sharpness_threshold:
            for _ in range(iterations if 0 < iterations < 10 else 5):
                while True:
                    match enhancer:
                        case "pillow":
                            print(f"Pillow - Image name: {image_enhancement}")
                            image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                      PillowEnhancer(),
                                                                                      kernel)
                            break
                        case "opencv":
                            print(f"OpenCV - Image name: {image_enhancement}")
                            image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                      OpencvEnhancer(),
                                                                                      kernel)
                            break
                        case "both":
                            print(f"Combined enhancing - Image name: {image_enhancement}")
                            image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                      PillowEnhancer(),
                                                                                      kernel,
                                                                                      True)
                            image_enhancement = self._image_manipulator.enhance_image(image_enhancement,
                                                                                      OpencvEnhancer(),
                                                                                      kernel,
                                                                                      True)
                            break
                        case _:
                            print("Please enter a valid value.")
                            enhancer = input("Which enhancer do you want to use? (pillow, opencv) ")
                            continue
        else:
            print(f"Image: {image_enhancement} - Should be able to be processed as is.")

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

    def give_documents_mock(self):
        documents = []
        for index in range(randrange(1, 5)):
            documents.append({
                "structured": self.give_structured(),
                "raw": {},
                "code": random.randint(0, 100),
                "rules": []
            })
        return documents

    @staticmethod
    def give_structured():
        return {
            "banco": "Bancolombia",
            "cliente": {
                "nombre": "Luis Garcia",
                "direccion": "CL 45",
                "barrio": "CL 45",
                "ciudad": "CL 45",
            },
            "cuenta": {
                "numero": "",
                "tipo": "",
                "origen": {
                    "codigo": "",
                    "nombre": "Bogota"
                },
            },
            "extracto": {
                "fecha": {
                    "desde": "",
                    "hasta": "",
                }
            },
            "resumen": {
                "saldo_inicial": "",
                "abonos": {
                    "cantidad": "",
                    "valor": "",
                },
                "cargos": {
                    "cantidad": "",
                    "valor": "",
                },
                "iva": "",
                "gmf": "",
                "retencion": "",
                "intereses": "",
                "saldo_final": "",
            },
            "movimientos": [
                {
                    "tipo": "(cargo/abono/intereses/otros… en caso de ser posible)",
                    "fecha": "",
                    "codigo": "",
                    "descripcion": "",
                    "ciudad": "",
                    "oficina": "",
                    "documento": "",
                    "valor": "",
                    "saldo": "",
                },
            ]
        }
