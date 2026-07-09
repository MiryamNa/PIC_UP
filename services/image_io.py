import cv2
import numpy as np

def safe_imread(path: str):
    """
    קריאה בטוחה לתמונה ב-Windows + תמיכה בעברית בקבצים.
    לא נופל אם הקובץ שבור או הנתיב לא תקין.
    """
    try:
        data = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_COLOR)

        if img is None:
            return None

        return img

    except Exception:
        return None

def safe_imread_gray(path: str):
    """
    Like safe_imread but returns a grayscale image.
    """
    try:
        data = np.fromfile(path, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
        return img if img is not None else None
    except Exception:
        return None

def safe_imwrite(path: str, img: np.ndarray):
    """
    כתיבה בטוחה לתמונה ב-Windows + תמיכה בעברית בנתיב.
    """
    try:
        ext = path.rsplit('.', 1)[-1]
        success, data = cv2.imencode(f'.{ext}', img)
        if not success:
            return False
        data.tofile(path)
        return True
    except Exception:
        return False

