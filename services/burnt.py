import cv2
import numpy as np
from services.image_io import safe_imread

class Burnt:
    @staticmethod
    def burnt_score(image_path=None,
                    image=None,
                    threshold: int = 240,
                    weight: float = 1.2) -> float:
        """
        Returns:
            float: score in [0, 1]
            1.0 = good image (not burnt)
            0.0 = very burnt / overexposed
        """

        if image is None:
            image = safe_imread(image_path)

        if image is None:
            raise ValueError(f"Image not loaded: {image_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # ratio of overexposed pixels
        bright_ratio = np.mean(gray >= threshold)

        # clamp extreme values for stability
        bright_ratio = np.clip(bright_ratio, 0.0, 0.8)

        # convert to quality score (higher = better)
        quality = 1.0 - (bright_ratio * weight)

        return float(np.clip(quality, 0.0, 1.0))


