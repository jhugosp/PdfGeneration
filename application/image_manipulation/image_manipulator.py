from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from skimage.util import img_as_float
from skimage.restoration import estimate_sigma
from skimage.measure import shannon_entropy
from domain.models.enhancers.image_enhancer import ImageEnhancer
from PIL import Image
import numpy
import cv2
import os


class ImageManipulator:

    @staticmethod
    def pdf_to_png(pdf_path, output_folder, index):
        """
        Converts a PDF file to PNG images and saves them to the specified output folder.

        Parameters:
        pdf_path (str): The file path of the input PDF file.
        output_folder (str): The directory where the PNG images will be saved.
        index (int): An index used to generate unique filenames for the extracted images.

        Functionality:
        1. Checks if the output folder exists; if not, it creates it.
        2. Uses pdf2image library to convert the PDF to a list of PIL Image objects.
        3. Iterates over the list of images and saves each one as a PNG file in the output folder.

        Note:
        - This method requires the pdf2image library to be installed (`pip install pdf2image`).

        Example:
        PDFProcessor.pdf_to_png("input.pdf", "output_folder", 1)
        """
        #   TODO: Do not save image, pass down as byte array in a different format
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = convert_from_path(pdf_path)
        pages = []
        for i, image in enumerate(images):
            image_name = f"extract_{i + 1}_{index}.png"
            image.show(image_name)
            pages.append(image)
        return pages

    @staticmethod
    def _calculate_blurriness(image):
        """
       Calculate the blurriness of an image using the variance of Laplacian method.

       Parameters:
       image: A NumPy array representing the input image.

       Returns:
       float: The variance of the Laplacian, indicating the blurriness of the image.

       Functionality:
       1. Converts the input image to grayscale using cv2.cvtColor.
       2. Calculates the Laplacian of the grayscale image using cv2.Laplacian.
       3. Computes the variance of the Laplacian using the var method.
       4. Returns the calculated blurriness value.

       Note:
       - A higher variance value indicates a sharper image, while a lower value indicates a blurrier image.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        return laplacian_var

    @staticmethod
    def _estimate_noise(image):
        """
        Estimates the noise level in an image.

        Parameters:
        image: A NumPy array representing the input image.

        Returns:
        float: The estimated noise level in the image.

        Functionality:
        1. Converts the input image to a floating-point representation using img_as_float.
        2. Estimates the noise level using the estimate_sigma function.
        3. Computes the mean of the estimated noise values.
        4. Returns the estimated noise level.

        Note:
        - The noise level is typically measured in standard deviation units.
        """
        image = img_as_float(image)
        sigma_est = numpy.mean(estimate_sigma(image=image, channel_axis=3))
        return sigma_est

    @staticmethod
    def _calculate_sharpness(image):
        """
        Calculates the sharpness of an image using Shannon entropy.

        Parameters:
        image: A NumPy array representing the input image.

        Returns:
        float: The calculated sharpness value of the image.

        Functionality:
        1. Converts the input image to grayscale using cv2.cvtColor.
        2. Calculates the Shannon entropy of the grayscale image using shannon_entropy.
        3. Returns the calculated sharpness value.

        Note:
        - A higher sharpness value indicates a more detailed and less blurry image.
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sharpness = shannon_entropy(gray)
        return sharpness

    @staticmethod
    def assess_image_quality(image):
        """
        Assess the quality of the image based on blurriness, noise, and sharpness.

        Parameters:
        image: The image file to assess.

        Returns:
        tuple: A tuple containing the calculated blurriness, noise, and sharpness values.

        Functionality:
        1. Reads the image from the specified file path using cv2.imread.
        2. Calculates the blurriness of the image using the _calculate_blurriness method.
        3. Estimates the noise level in the image using the _estimate_noise method.
        4. Calculates the sharpness of the image using the _calculate_sharpness method.
        5. Prints the calculated blurriness, noise, and sharpness values.
        6. Returns a tuple containing the calculated blurriness, noise, and sharpness values.

        Note:
        - The quality of the image can be assessed based on the calculated blurriness, noise, and sharpness values.
        """
        if isinstance(image, Image.Image):
            image = cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2GRAY)
        elif isinstance(image, numpy.ndarray):
            if image.ndim == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blurriness = ImageManipulator._calculate_blurriness(image)
        noise = ImageManipulator._estimate_noise(image)
        sharpness = ImageManipulator._calculate_sharpness(image)

        print(f"Blurriness: {blurriness}")
        print(f"Noise: {noise}")
        print(f"Sharpness: {sharpness}")

        return blurriness, noise, sharpness

    @staticmethod
    def enhance_image(image, image_enhancer: ImageEnhancer, kernel_option, combined=False) -> str:
        """
        Enhances an image using various image enhancement techniques.

        Parameters:
        image: The input image.

        Returns:
        str: The file enhanced image.

        Functionality:
        1. Prints the path of the distorted quality image and assesses its quality using the assess_image_quality method
        2. Reads the input image as grayscale using cv2.imread.
        3. Applies various image enhancement techniques:
           - Median blur using cv2.medianBlur.
           - Average blur using cv2.blur.
           - Non-local means denoising using cv2.fastNlMeansDenoising.
           - Sharpening using a custom sharpening kernel with cv2.filter2D.
           - Erosion using cv2.erode.
           - Contrast enhancement and sharpening using PIL ImageEnhance and ImageFilter.
           - Convolution with a custom kernel using PIL ImageFilter.Kernel.

        Note:
        - This method applies multiple image enhancement techniques iteratively to de-blur the input image.
        """
        kernel, size = ImageEnhancer.manage_sharpening_kernel(kernel_option)
        img = image_enhancer.enhance_image(image, kernel, size, combined)
        ImageManipulator.assess_image_quality(img)

        return img
