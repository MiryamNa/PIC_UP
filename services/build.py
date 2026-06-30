# """
# בנייה ועיבוד דמויות
# המטרה שלה:
# לפי השם והקוד, היא נועדה ליצור מופע של אירוע עבור לקוח ולעבד את כל התמונות שלו בעזרת המחלקה Build.
# היא אמורה:
# לקבל מזהה לקוח (custId) ומזהה אירוע (eventId).
# לקרוא את האירוע מה־service (event_service.get_event_by_id) כדי לדעת איפה התמונות מאוחסנות (eventCust.path).
# לקרוא את המתודה build_event_images() שמבצעת עיבוד לכל התמונות (חישוב burnt_score ו־sharpness_score) ומחזירה רשימה של תוצאות.
# """
# import os
#
# os.environ["INSIGHTFACE_HOME"] = r"C:\projects\AI_MODELS\insightface"
#
# import cv2
# from pathlib import Path
# from typing import Dict, Any, List
# from models import event
# from services.event_service import EventService
# from services.rename_images import clean_filename
# from services.burnt import Burnt
# from services.sharpness import Sharpness
# #from services.close_eyes import detect_closed_eyes
# # from services.selected_people_score import calculate_selected_people_score
# from repository.people_repository import people_repository
# from services.people_match import match_selected_people
# # from services.selected_people import get_face_embedding
# # from services.ml_config import *
# # from services.ml_config import INSIGHTFACE_HOME
#
# burnt = Burnt()
# sharpness = Sharpness()
#
# class Build:
#     cust_id: int
#     event_id: int
#     path: str
#     eventCust:event
#     book:Dict[str, Any]
#
#     def __init__(self, cust_id: int, event_id: int, path: str):
#         self.cust_id = cust_id
#         self.event_id = event_id
#         self.path = path
#
#     async def build_event_images(self) -> List[Dict[str, Any]]:
#         """
#         בנה דמויות לאירוע ספציפי של לקוח
#         עבור על כל תמונה, חשב את ציון burnt וחזר עם רשימה של ניתוב וציון
#
#         :param path: נתיב לתיקיית התמונות
#         :param cust_id: מזהה הלקוח
#         :param event_id: מזהה האירוע
#         :return: dict עם תוצאות העיבוד וציוני burnt עבור כל תמונה
#         """
#         # ניקוי שמות קבצים
#         clean_filename(self.path)
#         # בדיקה שהנתיב קיים
#         if not os.path.exists(self.path):
#             return {
#                 "status": "error",
#                 "message": f"הנתיב לא קיים: {self.path}",
#                 "cust_id": self.cust_id,
#                 "event_id": self.event_id
#             }
#
#         # בדיקה שהנתיב הוא תיקייה
#         if not os.path.isdir(self.path):
#             return {
#                 "status": "error",
#                 "message": f"הנתיב אינו תיקייה: {self.path}",
#                 "cust_id": self.cust_id,
#                 "event_id": self.event_id
#             }
#         if not os.path.exists(self.path):
#             return {
#                 "status": "error",
#                 "message": f"הנתיב לא קיים: {self.path}"
#             }
#
#         # קבלת רשימת התמונות
#         try:
#             images = [f for f in os.listdir(self.path)
#                       if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp'))]
#         except Exception as e:
#             return {
#                 "status": "error",
#                 "message": f"שגיאה בקריאת התיקייה: {str(e)}",
#                 "cust_id": self.cust_id,
#                 "event_id": self.event_id
#             }
#
#         # עיבוד כל תמונה וחישוב ציון burnt
#         mark_results: List[Dict[str, Any]] = []
#         categories = {
#             "out": {"images": []},
#             # "chuppa": {"images": []},
#             # "bride_chair": {"images": []},
#             # "yichud": {"images": []},
#             # "meal": {"images": []},
#             # "dance": {"images": []},
#             # "mizve_tanz": {"images": []},
#             # "noCategory": {"images": []}
#         }
#         for image in images:
#             clean_name = "".join(c for c in image if c.isprintable())
#             full_path = Path(self.path) / clean_name
#             full_path_str = str(full_path.resolve())
#
#             # צור נתיב מלא עם Path
#             full_path = Path(self.path) / image
#
#             # המרת הנתיב למחרוזת Unicode
#             full_path_str = str(full_path.resolve())
#
#             # קריאה לתמונה
#             img = cv2.imread(full_path_str, cv2.IMREAD_COLOR)
#
#             # אם התמונה לא נטענה, דלג על התמונה הזו
#             if img is None:
#                 print(f"Cannot read image: {full_path}")
#                 continue
#             full_path = os.path.join(self.path, image)
#
#             selected_embeddings = await people_repository.get_selected(
#                 self.cust_id,
#                 self.event_id
#             )
#             # try:
#             # כאן נזמן את הפונקציה שתקבע קטגוריה
#             # category=machineLearning-פונקציה שמחזירה את שם המערך
#             # כאן נכניס את התמונה למקום המתאים במערך
#             # categories[category]["images"].append(full_path)
#             # except Exception as e:
#             # טיפול אם יש שגיאה
#             categories["out"]["images"].append(full_path)
#         #close_eyes_detector = detect_closed_eyes()
#
#         for category in categories:
#             category_images = categories[category]["images"]
#             for image in category_images:
#                 burnt_score_value = burnt.burnt_score(image_path=image)
#                 sharpness_value = sharpness.calculate_sharpness_laplacian(image_path=image)
#                 selected_people_score = 0.0
#
#                 if category == "dance":
#                     selected_people_score = (
#                         calculate_selected_people_score(
#                             image_path=full_path,
#                             selected_embeddings=selected_embeddings
#                         )
#                     )
#                 """
#                 closed_eyes_score = None
#                 if category in ("bride_chair", "yichud", "meal"):
#                     closed_eyes_score = close_eyes_detector.detect_closed_eyes(image_path=image)
#
#                 """
#         for image in images:
#             full_path = os.path.join(self.path, image)
#
#             try:
#                 # כאן נזמן את הפונקציה שתקבע קטגוריה
#                 # category=machinLearning-פונקציה שמחזירה את שם המערך
#                 # כאן נכניס את התמונה למקום המתאים במערך
#                 # categories[category]["images"].append(full_path)
#                 burnt_score_value = burnt.burnt_score(image_path=full_path)
#                 sharpness_value = sharpness.calculate_sharpness_laplacian(image_path=full_path)
#                 mark_results.append({
#                     "image_path": full_path,
#                     "image_name": image,
#                     "burnt_score": burnt_score_value,
#                     "sharpness_score": sharpness_value,
#                     #"closed_eyes_score": closed_eyes_score,
#                     "selected_people_score": selected_people_score
#
#                 })
#
#             except Exception as e:
#                 mark_results.append({
#                     "image_path": full_path,
#                     "image_name": image,
#                     "burnt_score": None,
#                     "sharpness_score": None,
#                     "error": str(e)
#                 })
#
#         # בנייה וחזרה של התוצאות
#         return mark_results
#
# #running
# custId = 1
# eventId = 1
#
# # צור מופע של Build
# builder = Build(
#     cust_id=custId,
#     event_id=eventId,
#     path=r"O:\share\project miri and brachy\chassid\out"
# )
# # הרץ את הפונקציה לעיבוד התמונות
#
# book = builder.build_event_images()
#
# # הדפס את התוצאות
# # for r in book:
# #     print(r)
