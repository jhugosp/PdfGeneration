from domain.models.enhancers.image_enhancer import ImageEnhancer
from PIL import Image, ImageFilter, ImageEnhance


class PillowEnhancer(ImageEnhancer):

    def enhance_image(self, image_path, img_name):
        """ Enhances image by using pillow library through using various methods such as sharpening, denoising and
            blurring.

        :param image_path:  Path in which we find the image
        :param img_name:    The name which we will save the image under.
        :return:            Image path, in order to continue following enhancements.
        """
        img = Image.open(fp=image_path)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.filter(ImageFilter.SHARPEN)
        img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=150, threshold=5))

        kernel, size = super().manage_sharpening_kernel()

        img = img.filter(ImageFilter.Kernel(size=(size, size), kernel=kernel.flatten()))

        img_path = f"application/data_generation/generated_images/image_enhancement/pillow/{img_name}.png"
        img.save(fp=img_path)
        return img_path
