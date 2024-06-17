import os
from domain.models.converter.pdf_converter import PDFConverter
from pdf2image import convert_from_path
from PIL import Image


class FileToPNGConverter(PDFConverter):
    """
    Converts PDF, JPG, and JPEG files to PNG images.
    """
    def convert(self, input_folder, output_folder):
        """
        Converts PDF, JPG, and JPEG files to PNG images and saves them in the specified output folder.
        If the file is already in PNG format, it is copied without modification.

        Args:
            input_folder (str): The path to the folder containing the files to be converted.
            output_folder (str): The path to the folder where the PNG images will be saved.
        """
        #   TODO: validate conversion but not saving of file, return as byte array

        # Check if the output folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through each file in the specified input folder
        for filename in os.listdir(input_folder):
            full_path = os.path.join(input_folder, filename)
            if filename.endswith(".pdf"):
                try:
                    # Attempt to convert the PDF file to a list of PIL images
                    images = convert_from_path(full_path)
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"Skipping invalid PDF file: {filename}")
                    continue

                # Save each generated image as a PNG file in the output folder
                for i, image in enumerate(images):
                    image_name = f"{os.path.splitext(filename)[0]}_{i}.png"
                    image_path = os.path.join(output_folder, image_name)
                    image.save(image_path, 'PNG')
                    print(f"Saved Image: {image_name}")
            elif filename.lower().endswith((".jpg", ".jpeg")):
                try:
                    with Image.open(full_path) as img:
                        image_name = f"{os.path.splitext(filename)[0]}.png"
                        image_path = os.path.join(output_folder, image_name)
                        img.save(image_path, 'PNG')
                        print(f"Converted and saved Image: {image_name}")
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"Skipping invalid image file: {filename}")
                    continue
            elif filename.lower().endswith(".png"):
                try:
                    # Copy PNG files to the output folder without modification
                    image_name = filename
                    image_path = os.path.join(output_folder, image_name)
                    with Image.open(full_path) as img:
                        img.save(image_path, 'PNG')
                    print(f"Copied Image: {image_name}")
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"Skipping invalid PNG file: {filename}")
                    continue

