from domain.models.enhancers.image_enhancer import ImageEnhancer
import albumentations as A
import cv2


class OpencvEnhancer(ImageEnhancer):

    def enhance_image(self, image_path, kernel, size, combined=False):
        """ Enhances image by using opencv - cv2 library through using various methods such as sharpening, denoising,
            blurring and 2D filtering.

        :param size:
        :param kernel:
        :param combined:    Indication if the image in case was pre-processed by Pillow as well, changing store path.
        :param image_path:  Path in which we find the image.
        :return:            Image path, in order to continue following enhancements.
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        augmentations = A.Compose([
            A.CLAHE(clip_limit=2.0, p=1.0),
            A.Sharpen(alpha=(0.2, 0.5), lightness=(0.5, 1.0), p=1.0),
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.5),
        ])
        augmented = augmentations(image=img)
        img = augmented['image']

        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.fastNlMeansDenoising(img, None, h=10, templateWindowSize=7, searchWindowSize=21)

        img = cv2.filter2D(img, -1, kernel)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        img = cv2.erode(img, kernel, iterations=1)
        img = cv2.dilate(img, kernel, iterations=1)
        cv2.imshow("", img)
        return img
