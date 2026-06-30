# # services/selected_people.py
#
# import cv2
# import numpy as np
# # from insightface.app import FaceAnalysis
#
# # app = FaceAnalysis(name="buffalo_l")
# app.prepare(ctx_id=0, det_size=(640, 640))
#
#
# def get_face_embedding(image_path: str):
#
#     img = cv2.imread(image_path)
#
#     if img is None:
#         return None
#
#     faces = app.get(img)
#
#     if not faces:
#         return None
#
#     face = max(
#         faces,
#         key=lambda f:
#         (f.bbox[2] - f.bbox[0]) *
#         (f.bbox[3] - f.bbox[1])
#     )
#
#     return face.embedding
#
# selected_embeddings = []

