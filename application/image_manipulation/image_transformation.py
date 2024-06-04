from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from skimage.util import img_as_float
from skimage.restoration import estimate_sigma
from skimage.measure import shannon_entropy
import numpy
import cv2
import os


class ImageManipulator:

    @staticmethod
    def distort_image(image_path, distortion_type, threshold=240):
        image = Image.open(image_path)
        image = image.convert("L")
        if distortion_type:
            image = image.filter(ImageFilter.GaussianBlur(0.3))
        else:
            image = image.point(lambda x: 255 if x > threshold else 0)

        return image

    @staticmethod
    def image_to_pdf(image, pdf_path):
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        # image = image.resize((width, height), Image.LANCZOS)
        image_path = 'temp_image.jpg'
        image.save(image_path)
        c.drawImage(image_path, 0, 0, width, height)
        c.save()

    @staticmethod
    def list_files_in_directory(directory):
        with os.scandir(directory) as entries:
            files = [entry.name for entry in entries if entry.is_file()]
        return files

    @staticmethod
    def pdf_to_png(pdf_path, output_folder, index):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"extract_{i + 1}_{index}.png")
            image.save(image_path, 'PNG')

    @staticmethod
    def generate_distorted_images():
        consulted_dir = input("Which directory will you consult? (distorted_1/distorted_2) ")
        dir_path = f"application/data_generation/distorted_pdfs/{consulted_dir}"
        extracted_files: [] = ImageManipulator.list_files_in_directory(dir_path)
        for index_file in range(len(extracted_files)):
            ImageManipulator.pdf_to_png(
                f'{dir_path}/{extracted_files[index_file]}',
                f'application/data_generation/generated_images/{consulted_dir}',
                (index_file + 1)
            )
            print(f"Successfully printed image: {index_file + 1}")

    @staticmethod
    def _calculate_blurriness(image):
        """Calculate the variance of the Laplacian to assess blurriness."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var

    @staticmethod
    def _estimate_noise(image):
        """Estimate the noise level of the image using scikit-image."""
        image = img_as_float(image)
        sigma_est = numpy.mean(estimate_sigma(image=image, channel_axis=3))
        return sigma_est

    @staticmethod
    def _calculate_sharpness(image):
        """Calculate the sharpness of the image using entropy."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpness = shannon_entropy(gray)
        return sharpness

    @staticmethod
    def assess_image_quality(image_path):
        """Assess the quality of the image."""
        image = cv2.imread(image_path)

        blurriness = ImageManipulator._calculate_blurriness(image)
        noise = ImageManipulator._estimate_noise(image)
        sharpness = ImageManipulator._calculate_sharpness(image)

        print(f"Blurriness: {blurriness}")
        print(f"Noise: {noise}")
        print(f"Sharpness: {sharpness}")

        return blurriness, noise, sharpness

    @staticmethod
    def _apply_high_pass_filter(image):
        low_pass = cv2.GaussianBlur(image, (21, 21), 3)
        high_pass = cv2.addWeighted(image, 1.5, low_pass, -0.5, 0)
        return high_pass

    @staticmethod
    def de_blur_image(image_path, iterations) -> str:
        print(f"Distorted quality image: {image_path}")
        ImageManipulator.assess_image_quality(image_path=image_path)

        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        img = cv2.medianBlur(img, 3)
        img = cv2.blur(img, (3, 3))
        img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

        img = ImageManipulator._apply_high_pass_filter(img)

        sharpening_kernel = numpy.array([[-1, -1, -1, -1, -1],
                                         [-1, 2, 2, 2, -1],
                                         [-1, 2, 8, 2, -1],
                                         [-1, 2, 2, 2, -1],
                                         [-1, -1, -1, -1, -1]]) / 8.0

        img = cv2.filter2D(img, -1, sharpening_kernel)

        kernel = numpy.ones((2, 1), numpy.uint8)
        img = cv2.erode(img, kernel, iterations=1)

        img = Image.fromarray(img)

        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=150, threshold=5))

        kernel = numpy.array([[-1, -2, -1],
                              [-2, -16, -2],
                              [-1, -2, -1]])

        img = img.filter(ImageFilter.Kernel(size=(3, 3), kernel=kernel.flatten()))

        img_name = f"image_{iterations}"
        img_path = f"application/data_generation/generated_images/image_enhancement/{img_name}.png"
        img.save(fp=img_path)

        return img_path
