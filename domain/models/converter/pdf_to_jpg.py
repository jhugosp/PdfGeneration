import os
from domain.models.converter.pdf_converter import PDFConverter
from pdf2image import convert_from_path


class PDFToJPGConverter(PDFConverter):
    def convert(self, pdf_path, output_folder):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for filename in os.listdir(pdf_path):
            if filename.endswith(".pdf"):
                full_path = os.path.join(pdf_path, filename)
                try:
                    images = convert_from_path(full_path)
                except Exception as e:
                    print(f"Error: {e}")
                    print(f"Skipping invalid PDF file: {filename}")
                    continue

                for i, image in enumerate(images):
                    image_name = f"{os.path.splitext(filename)[0]}_page_{i + 1}.jpg"
                    image_path = os.path.join(output_folder, image_name)
                    image.save(image_path, 'JPEG')
                    print(f"Saved Image: {image_name}")

