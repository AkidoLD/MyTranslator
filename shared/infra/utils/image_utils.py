from tkinter import PhotoImage

import PIL
from PIL import ImageTk, Image as ImageP
from PIL.Image import Resampling, Image
from PIL.ImageFile import ImageFile


class ImageUtils:

    @staticmethod
    def get_image(image_path, size : int | tuple[int, int] = None) -> Image:
        try :
            image = ImageP.open(image_path)
            if size is not None :
                image = image.resize((size, size) if isinstance(size, int) else size, Resampling.LANCZOS)
            return image
            #
        except (FileNotFoundError, PIL.UnidentifiedImageError, ValueError, TypeError) as e :
            raise RuntimeError(f"An error occurred while retrieving the image : {e}")

    @staticmethod
    def convert_to_tk_image(image_file : Image, size : int | tuple[int, int] = None, rotation : int = None) -> PhotoImage:
        if size is not None :
            image_file = image_file.resize((size, size) if isinstance(size, int) else size, Resampling.LANCZOS)
        if rotation is not None :
            image_file = image_file.rotate(rotation, Resampling.LANCZOS, True)
        return ImageTk.PhotoImage(image_file)

    @staticmethod
    def get_tk_image(image_path, size : int | tuple[int, int] = None, angle : int = None):
        return ImageUtils.convert_to_tk_image(ImageUtils.get_image(image_path), size, angle)
