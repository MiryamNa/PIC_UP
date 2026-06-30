"""
import os
import cv2
from PIL import Image
from insightface.app import FaceAnalysis


def extract_single_faces(folder_path):
    results = []

    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img = cv2.imread(file_path)
        if img is None:
            continue

        faces = app.get(img)

        if len(faces) != 1:
            continue

        face = faces[0]
        x1, y1, x2, y2 = map(int, face.bbox)

        cropped = img[y1:y2, x1:x2]
        cropped_pil = Image.fromarray(cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB))

        results.append((cropped_pil, face.embedding))

    return results
"""
import os
import cv2
from PIL import Image
from insightface.app import FaceAnalysis

def extract_single_faces(folder_path):
    results = []

    app = FaceAnalysis(providers=['CPUExecutionProvider'])
    app.prepare(ctx_id=0, det_size=(640, 640))

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if not file_name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        img = cv2.imread(file_path)
        if img is None:
            continue

        faces = app.get(img)

        # רק תמונות עם פנים יחידה
        if len(faces) != 1:
            continue

        face = faces[0]
        x1, y1, x2, y2 = map(int, face.bbox)

        # =========================
        # תיקון גבולות תמונה
        # =========================
        h, w = img.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(w, x2)
        y2 = min(h, y2)

        # וידוא crop תקין
        if x2 <= x1 or y2 <= y1:
            continue

        # =========================
        # padding לפנים (שיפור איכות)
        # =========================
        pad = 10
        x1 = max(0, x1 - pad)
        y1 = max(0, y1 - pad)
        x2 = min(w, x2 + pad)
        y2 = min(h, y2 + pad)

        # =========================
        # crop + תיקון צבע
        # =========================
        cropped = img[y1:y2, x1:x2]
        cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2RGB)

        cropped_pil = Image.fromarray(cropped)

        results.append((cropped_pil, face.embedding))

    return results
