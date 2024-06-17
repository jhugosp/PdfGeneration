import os
from domain.models.converter.pdf_converter import PDFConverter
from pdf2image import convert_from_path


class PDFToPNGConverter(PDFConverter):
    """
    Converts PDF files to PNG images.
    """
    def convert(self, pdf_path, output_folder):
        """
         Converts PDF files to PNG images and saves them in the specified output folder.

         Args:
             pdf_path (str): The path to the folder containing the PDF files to be converted.
             output_folder (str): The path to the folder where the PNG images will be saved.
         """
        #   TODO: validate conversion but not saving of file, return as byte array
        # Check if the output folder exists, if not, create it
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Iterate through each file in the specified PDF folder
        for filename in os.listdir(pdf_path):
            if filename.endswith(".pdf"):
                full_path = os.path.join(pdf_path, filename)
                try:
                    # Attempt to convert the PDF file to a list of PIL images
                    images = convert_from_path(full_path)
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"Skipping invalid PDF file: {filename}")
                    continue

                # Save each generated image as a PNG file in the output folder
                for i, image in enumerate(images):
                    image_name = f"{os.path.splitext(filename)[0]}.png"
                    image_path = os.path.join(output_folder, image_name)
                    image.save(image_path, 'PNG')
                    print(f"Saved Image: {image_name}")
