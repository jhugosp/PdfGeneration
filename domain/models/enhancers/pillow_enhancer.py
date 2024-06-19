from domain.models.enhancers.image_enhancer import ImageEnhancer
from PIL import Image, ImageFilter, ImageEnhance


class PillowEnhancer(ImageEnhancer):

    def enhance_image(self, image_path, kernel, size, combined=False):
        """ Enhances image by using pillow library through using various methods such as sharpening, denoising and
            blurring.

        :param kernel:
        :param size:
        :param combined:    Indication if the image in case was pre-processed by Pillow as well, changing store path.
        :param image_path:  Path in which we find the image.
        :return:            Image path, in order to continue following enhancements.
        """
        img = Image.open(fp=image_path).convert("L")
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=150, threshold=0))

        img = img.filter(ImageFilter.Kernel(size=(size, size), kernel=kernel.flatten()))
        img.show()
        return img
