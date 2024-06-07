from domain.models.enhancers.image_enhancer import ImageEnhancer
import numpy
import cv2


class OpencvEnhancer(ImageEnhancer):

    def enhance_image(self, image_path, img_name):
        """ Enhances image by using opencv - cv2 library through using various methods such as sharpening, denoising,
            blurring and 2D filtering.

        :param image_path:  Path in which we find the image
        :param img_name:    The name which we will save the image under.
        :return:            Image path, in order to continue following enhancements.
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        img = cv2.medianBlur(img, 3)
        img = cv2.blur(img, (3, 3))
        img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

        sharpening_kernel = numpy.array([[-1, -1, -1, -1, -1],
                                         [-1, 2, 2, 2, -1],
                                         [-1, 2, 8, 2, -1],
                                         [-1, 2, 2, 2, -1],
                                         [-1, -1, -1, -1, -1]]) / 8.0

        img = cv2.filter2D(img, -1, sharpening_kernel)

        kernel = numpy.ones((2, 1), numpy.uint8)
        img = cv2.erode(img, kernel, iterations=1)
        img_path = f"application/data_generation/generated_images/image_enhancement/opencv/{img_name}.png"
        cv2.imwrite(img_path, img)

        return img_path
