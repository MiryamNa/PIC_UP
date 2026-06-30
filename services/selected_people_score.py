# import cv2
# import numpy as np
#
# from insightface.app import FaceAnalysis
#
# app = FaceAnalysis(name="buffalo_l")
# app.prepare(ctx_id=0, det_size=(640, 640))
#
#
# def calculate_selected_people_score(
#     image_path,
#     selected_embeddings,
#     threshold=0.6
# ):
#     img = cv2.imread(image_path)
#
#     if img is None:
#         return 0.0
#
#     faces = app.get(img)
#
#     if not faces:
#         return 0.0
#
#     matched_people = set()
#
#     for face in faces:
#
#         embedding = face.embedding
#
#         for idx, selected in enumerate(selected_embeddings):
#
#             dist = np.linalg.norm(
#                 embedding - selected
#             )
#
#             if dist < threshold:
#
#                 matched_people.add(idx)
#
#     return (
#         len(matched_people)
#         /
#         len(selected_embeddings)
#    )