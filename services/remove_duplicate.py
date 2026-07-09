import numpy as np
import cv2
from insightface.app import FaceAnalysis
import base64



def _to_numpy(img):
    """המרת תמונה לכל פורמט תקין"""
    if img is None:
        return None

    if hasattr(img, "convert"):
        img = np.array(img.convert("RGB"))

    if len(img.shape) == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)

    return img


def to_base64(images):
    encoded_images = []

    for pil_img in images:
        img = np.array(pil_img)

        # 🔥 חשוב מאוד: RGB → BGR לפני encode
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        _, buffer = cv2.imencode(".jpg", img)

        encoded = base64.b64encode(buffer).decode("utf-8")
        encoded_images.append(encoded)

    return encoded_images


def remove_duplicate_faces(face_data, similarity_threshold=0.6):

    if not face_data:
        return []

    embeddings = []
    unique_faces = []

    for img, emb in face_data:

        norm = np.linalg.norm(emb)

        # 🔥 הגנה על division by zero
        if norm == 0:
            continue

        emb = emb / norm
        emb = emb.astype(np.float32)

        is_duplicate = False

        for e in embeddings:
            if np.dot(emb, e) > similarity_threshold:
                is_duplicate = True
                break

        if not is_duplicate:
            embeddings.append(emb)
            unique_faces.append(img)

    return to_base64(unique_faces)