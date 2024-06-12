from abc import ABC, abstractmethod


class PDFConverter(ABC):
    @abstractmethod
    def convert(self, pdf_path, output_folder):
        pass
