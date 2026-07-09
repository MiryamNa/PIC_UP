





import cv2
import numpy as np
from services.image_io import safe_imread, safe_imread_gray

class Sharpness:
    @staticmethod
    def calculate_sharpness_laplacian(image_path=None, image=None):
        """
        Calculate sharpness using Laplacian variance.

        Args:
            image_path: Path to image file (used if image not provided)
            image: Numpy array of the image (BGR or grayscale).
                   When provided, skips disk read.

        Returns:
            float: Laplacian variance (higher = sharper)
        """
        if image is None:
            image = safe_imread_gray(image_path)
        elif len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        laplacian = cv2.Laplacian(image, cv2.CV_64F)
        return laplacian.var()








