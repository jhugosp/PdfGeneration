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
        """
        Applies a specified distortion to an image.

        Parameters:
        image_path (str): The file path to the image that you want to distort.
        distortion_type (bool): Determines the type of distortion to apply.
                                If True, applies a Gaussian blur to the image.
                                If False, applies a thresholding effect to the image.
        threshold (int, optional): The threshold value for the thresholding effect.
                                   Default is 240. This parameter is only used if distortion_type is False.

        Returns:
        PIL.Image.Image: The distorted image.
        """
        image = Image.open(image_path)
        image = image.convert("L")
        if distortion_type:
            image = image.filter(ImageFilter.GaussianBlur(0.3))
        else:
            image = image.point(lambda x: 255 if x > threshold else 0)

        return image

    @staticmethod
    def image_to_pdf(image, pdf_path):
        """
        Converts an image to a PDF and saves it to the specified path.

        Parameters:
        image (PIL.Image.Image): The image object to convert to PDF.
        pdf_path (str): The file path where the generated PDF should be saved.

        Functionality:
        1. Creates a Canvas object for PDF generation.
        2. Resizes the image to fit the dimensions of the letter-sized page.
        3. Draws the resized image onto the PDF canvas.
        4. Saves the Canvas, finalizing the PDF.
        """
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        image = image.resize((width, height), Image.LANCZOS)
        image_path = 'temp_image.jpg'
        image.save(image_path)
        c.drawImage(image_path, 0, 0, width, height)
        c.save()

    @staticmethod
    def list_files_in_directory(directory):
        """
        Lists all files in a directory.

        Parameters:
        directory (str): The path of the directory to list files from.

        Returns:
        list: A list of filenames present in the directory.

        Functionality:
        1. Uses os.scandir to iterate over the contents of the directory.
        2. Filters out only the files from the directory entries.
        3. Returns a list containing the names of the files.

        Example:
        files = list_files_in_directory("/path/to/directory")
        print(files)
        ['file1.txt', 'file2.jpg', 'file3.py']
        """
        with os.scandir(directory) as entries:
            files = [entry.name for entry in entries if entry.is_file()]
        return files

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
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        images = convert_from_path(pdf_path)

        for i, image in enumerate(images):
            image_path = os.path.join(output_folder, f"extract_{i + 1}_{index}.png")
            image.save(image_path, 'PNG')

    @staticmethod
    def generate_distorted_images():
        """
        Generates distorted images from PDF files in a specified directory.

        Functionality:
        1. Prompts the user to choose a directory to consult for distorted PDF files.
        2. Constructs the directory path based on the user's choice.
        3. Retrieves a list of PDF files in the specified directory using ImageManipulator.list_files_in_directory
        4. Iterates over each PDF file in the directory:
           - Converts the PDF file to PNG images using the ImageManipulator.pdf_to_png method.
           - Saves the generated PNG images to the 'generated_images' directory with appropriate index.
        5. Prints a success message for each image generated.

        Note:
        - This method relies on the ImageManipulator class for listing files in a directory and converting
        PDF to PNG images
        """
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
    def assess_image_quality(image_path):
        """
        Assess the quality of the image based on blurriness, noise, and sharpness.

        Parameters:
        image_path (str): The file path of the image to assess.

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
        """
        Applies a high-pass filter to enhance edges in an image.

        Parameters:
        image: A NumPy array representing the input image.

        Returns:
        numpy.ndarray: The image with high-pass filter applied.

        Functionality:
        1. Applies a Gaussian blur to the input image using cv2.GaussianBlur.
        2. Computes the high-pass filter by subtracting the blurred image from the original image.
        3. Returns the resulting image with enhanced edges.

        Note:
        - A high-pass filter enhances the edges in an image by emphasizing high-frequency components.
        """
        low_pass = cv2.GaussianBlur(image, (21, 21), 3)
        high_pass = cv2.addWeighted(image, 1.5, low_pass, -0.5, 0)
        return high_pass

    @staticmethod
    def de_blur_image(image_path, iterations) -> str:
        """
        De-blurs an image using various image enhancement techniques.

        Parameters:
        image_path (str): The file path of the input image.
        iterations (int): The number of iterations for applying enhancement techniques.

        Returns:
        str: The file path of the de-blurred image.

        Functionality:
        1. Prints the path of the distorted quality image and assesses its quality using the assess_image_quality method.
        2. Reads the input image as grayscale using cv2.imread.
        3. Applies various image enhancement techniques:
           - Median blur using cv2.medianBlur.
           - Average blur using cv2.blur.
           - Non-local means denoising using cv2.fastNlMeansDenoising.
           - High-pass filter using the _apply_high_pass_filter method.
           - Sharpening using a custom sharpening kernel with cv2.filter2D.
           - Erosion using cv2.erode.
           - Contrast enhancement and sharpening using PIL ImageEnhance and ImageFilter.
           - Convolution with a custom kernel using PIL ImageFilter.Kernel.
        4. Saves the de-blurred image with the specified number of iterations.

        Note:
        - This method applies multiple image enhancement techniques iteratively to de-blur the input image.
        """
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
