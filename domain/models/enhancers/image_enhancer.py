from abc import abstractmethod, ABC


class ImageEnhancer(ABC):

    @abstractmethod
    def enhance_image(self, *args):
        pass
