from PIL import Image, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
from skimage.util import img_as_float
from skimage.restoration import estimate_sigma
from skimage.measure import shannon_entropy
import numpy
import os
import cv2


def list_files_in_directory(directory):
    with os.scandir(directory) as entries:
        files = [entry.name for entry in entries if entry.is_file()]
    return files


def pdf_to_png(pdf_path, output_folder, index):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    images = convert_from_path(pdf_path)

    for i, image in enumerate(images):
        image_path = os.path.join(output_folder, f"extract_{i + 1}_{index}.png")
        image.save(image_path, 'PNG')


def calculate_blurriness(image):
    """Calculate the variance of the Laplacian to assess blurriness."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var


def estimate_noise(image):
    """Estimate the noise level of the image using scikit-image."""
    image = img_as_float(image)
    sigma_est = numpy.mean(estimate_sigma(image=image, channel_axis=3))
    return sigma_est


def calculate_sharpness(image):
    """Calculate the sharpness of the image using entropy."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sharpness = shannon_entropy(gray)
    return sharpness


def assess_image_quality(image_path):
    """Assess the quality of the image."""
    image = cv2.imread(image_path)

    blurriness = calculate_blurriness(image)
    noise = estimate_noise(image)
    sharpness = calculate_sharpness(image)

    print(f"Blurriness: {blurriness}")
    print(f"Noise: {noise}")
    print(f"Sharpness: {sharpness}")

    return blurriness, noise, sharpness


def apply_high_pass_filter(image):
    low_pass = cv2.GaussianBlur(image, (21, 21), 3)
    high_pass = cv2.addWeighted(image, 1.5, low_pass, -0.5, 0)
    return high_pass


def de_blur_image(image_path, iterations) -> str:
    print(f"Distorted quality image: {image_path}")
    assess_image_quality(image_path=image_path)

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    img = cv2.medianBlur(img, 3)
    img = cv2.blur(img, (3, 3))
    img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

    img = apply_high_pass_filter(img)

    sharpening_kernel = numpy.array([[-1, -1, -1, -1, -1],
                                  [-1,  2,  2,  2, -1],
                                  [-1,  2,  8,  2, -1],
                                  [-1,  2,  2,  2, -1],
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
    img_path = f"generated_images/test/{img_name}.png"
    img.save(fp=img_path)

    return img_path

