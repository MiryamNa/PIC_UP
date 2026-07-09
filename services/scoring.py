import numpy as np
import threading
from services.burnt import Burnt
from services.sharpness import Sharpness
from services.closed_eyes_result import eye_closed_score
from insightface.app import FaceAnalysis
from services.image_io import safe_imread

burnt = Burnt()
sharpness = Sharpness()

# ---------- GPU auto-detection ----------
def _get_providers():
    """Auto-detect best available ONNX Runtime providers."""
    try:
        import onnxruntime as ort
        available = ort.get_available_providers()
        preferred = ['CUDAExecutionProvider', 'CPUExecutionProvider']
        return [p for p in preferred if p in available]
    except ImportError:
        return ['CPUExecutionProvider']

PROVIDERS = _get_providers()

# ---------- Thread-local FaceAnalysis (for parallel workers, Phase 2) ----------
_thread_local = threading.local()

def get_face_app():
    """Return a thread-local FaceAnalysis instance (lazy init)."""
    if not hasattr(_thread_local, "face_app"):
        _thread_local.face_app = FaceAnalysis(providers=PROVIDERS)
        _thread_local.face_app.prepare(ctx_id=0, det_size=(640, 640))
    return _thread_local.face_app

# Global instance for single-threaded use (backward compatible)
face_app = get_face_app()

# ---------- similarity ----------
def cosine_sim(a, b):
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)
    return np.dot(a, b)

# ---------- count matched faces ----------
def count_selected_faces(image=None,
                         selected_embeddings=None,
                         threshold=0.6):
    """
    Count how many faces in the image match the selected embeddings.

    Args:
        image: Numpy array of the image (BGR)
        selected_embeddings: List of face embeddings to match against
        threshold: Cosine similarity threshold for a match

    Returns:
        int: Number of matched faces
    """
    if image is None or not selected_embeddings:
        return 0

    faces = get_face_app().get(image)

    count = 0
    for face in faces:
        emb = face.embedding
        for target in selected_embeddings:
            if cosine_sim(emb, target) > threshold:
                count += 1
                break

    return count

# ---------- detect bride or groom ----------
def detect_bride_or_groom(image=None,
                          bride_embedding=None,
                          groom_embedding=None,
                          threshold=0.6):
    """
    Check whether the bride or groom appears in the image.

    Args:
        image: Numpy array of the image (BGR)
        bride_embedding: Face embedding of the bride (single vector)
        groom_embedding: Face embedding of the groom (single vector)
        threshold: Cosine similarity threshold for a match

    Returns:
        bool: True if bride or groom is detected in the image
    """
    if image is None:
        return False

    targets = []
    if bride_embedding is not None:
        targets.append(bride_embedding)
    if groom_embedding is not None:
        targets.append(groom_embedding)

    if not targets:
        return False

    faces = get_face_app().get(image)

    for face in faces:
        emb = face.embedding
        for target in targets:
            if cosine_sim(emb, target) > threshold:
                return True

    return False

# ---------- main scoring ----------
def get_image_score(image_path=None,
                    image=None,
                    selected_embeddings=None,
                    category=None,
                    bride_embedding=None,
                    groom_embedding=None):

    if image is None:
        image = safe_imread(image_path)
    if image is None:
        raise ValueError(f"Cannot read image: {image_path}")

    sharp = sharpness.calculate_sharpness_laplacian(image=image)
    bright = burnt.burnt_score(image=image)

    sharp_score = min(max(sharp / 1000, 0.0), 1.0)
    bright_score = min(max(bright / 100, 0.0), 1.0)

    face_score = 0.0
    matched = 0

    if selected_embeddings:
        matched = count_selected_faces(
            image=image,
            selected_embeddings=selected_embeddings
        )
        face_score = min(matched / 3.0, 1.0)

    # בדיקה האם החתן או הכלה מופיעים בתמונה
    has_bride_or_groom = False
    if category != "out":
        has_bride_or_groom = detect_bride_or_groom(
            image=image,
            bride_embedding=bride_embedding,
            groom_embedding=groom_embedding,
        )

    bonus = 0.05 if category in ["yichud", "meal", "bride_chair"] else 0.0

    base_score = (
        sharp_score * 0.50 +
        bright_score * 0.15 +
        face_score * 0.35 +
        bonus
    )

    # אם החתן/כלה נמצאו והקטגוריה אינה "out" — תוספת 50%
    if has_bride_or_groom:
        base_score += 0.50

    # חשוב: רק לקטגוריות מסוימות מחשבים eye model
    if category in ["yichud", "meal", "bride_chair"]:
        eye_penalty = eye_closed_score(image)
        final_score = base_score * (1.0 - eye_penalty * 0.10)
    else:
        final_score = base_score

    result = {
        "score": float(min(final_score, 1.0)),
        "category_name": category or "general",
    }

    # עבור meal ו-dance — הוסף זיהוי מגדר
    if category in ("meal", "dance"):
        from services.division_men_and_women import divide_men_and_women
        result["gender"] = divide_men_and_women(None)

    return result


