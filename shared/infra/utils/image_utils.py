from tkinter import PhotoImage

import PIL
from PIL import ImageTk, Image as ImageP
from PIL.Image import Resampling, Image
from PIL.ImageFile import ImageFile


class ImageUtils:

    @staticmethod
    def get_image(image_path, size : tuple[int, int] = None) -> Image:
        try :
            image = ImageP.open(image_path)
            if size is not None :
                image = image.resize(size, Resampling.LANCZOS)
            return image
            #
        except FileNotFoundError | PIL.UnidentifiedImageError | ValueError | TypeError as e :
            raise RuntimeError(f"An error occurred while retrieving the image : {e}")

    @staticmethod
    def image_file_to_tk_image(image_file : Image, size : tuple[int, int] = None, angle : int = None) -> PhotoImage:
        if size is not None :
            image_file = image_file.resize(size, Resampling.LANCZOS)
        if angle is not None :
            image_file = image_file.rotate(angle, Resampling.LANCZOS, True)
        return ImageTk.PhotoImage(image_file)
