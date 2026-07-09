import threading
import numpy as np
from insightface.app import FaceAnalysis

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

# ---------- Thread-local FaceAnalysis ----------
_thread_local = threading.local()

def _get_face_app():
    """Return a thread-local FaceAnalysis instance (lazy init)."""
    if not hasattr(_thread_local, "face_app"):
        _thread_local.face_app = FaceAnalysis(providers=PROVIDERS)
        _thread_local.face_app.prepare(ctx_id=0, det_size=(640, 640))
    return _thread_local.face_app

def eye_aspect_ratio(eye):
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])

    if C == 0:
        return 0.0

    return (A + B) / (2.0 * C)

def _face_size(landmarks_2d):
    xs = landmarks_2d[:, 0]
    ys = landmarks_2d[:, 1]

    return (xs.max() - xs.min()) * (ys.max() - ys.min())

def eye_closed_score(image):
    """
    Compute open-eyes score for all faces in an image.

    Uses InsightFace 68-point 3D landmarks (dlib-compatible indices).
    Left eye: 36–41, Right eye: 42–47.

    Args:
        image: np.ndarray (BGR, as loaded by cv2.imread)

    Returns:
        float in [0.0, 1.0]
        1.0 = all faces have open eyes
        0.0 = all faces closed / no faces detected
    """
    face_app = _get_face_app()
    faces = face_app.get(image)

    if len(faces) == 0:
        return 0.0

    weighted_scores = []
    weights = []

    for face in faces:
        lm = face.landmark_3d_68
        if lm is None:
            continue

        lm_2d = np.array(lm, dtype=np.float32)[:, :2]

        left_eye = lm_2d[36:42]
        right_eye = lm_2d[42:48]

        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)

        avg_ear = (left_ear + right_ear) / 2.0

        # Normalize EAR to [0, 1]
        # Open eyes: ~0.25–0.35, Closed: ~0.1–0.2
        score = float(np.clip((avg_ear - 0.15) / (0.35 - 0.15), 0.0, 1.0))

        size = _face_size(lm_2d)

        weighted_scores.append(score * size)
        weights.append(size)

    if sum(weights) == 0:
        return 0.0

    return float(sum(weighted_scores) / sum(weights))


