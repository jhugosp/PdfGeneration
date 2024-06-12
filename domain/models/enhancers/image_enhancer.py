import random
import numpy
from abc import abstractmethod, ABC


class ImageEnhancer(ABC):

    @abstractmethod
    def enhance_image(self, *args):
        pass

    @staticmethod
    def manage_sharpening_kernel():
        """ Randomly generates a pre-defined sharpening kernel

        :return:    A 3x3 or 5x5 sharpening kernel, more aggressive successively
        """
        probability = random.random()
        if probability < 0.5:
            return numpy.array([[0, -1, 0],
                                [-1, 5, -1],
                                [0, -1, 0]]), 3

        else:
            return numpy.array([[-1, -1, -1, -1, -1],
                                [-1, 2, 2, 2, -1],
                                [-1, 2, 8, 2, -1],
                                [-1, 2, 2, 2, -1],
                                [-1, -1, -1, -1, -1]]) / 8.0, 5
