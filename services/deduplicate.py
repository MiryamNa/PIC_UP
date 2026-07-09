"""
שירות למחיקת כפילויות — מזהה תמונות כפולות בתיקייה,
משאיר את התמונה האיכותית ביותר מכל קבוצת כפילויות,
ומעביר את השאר לתיקיית Junk.
"""
import os
import shutil
from collections import defaultdict
from typing import List

from PIL import Image
import imagehash

from services.sharpness import Sharpness
from services.burnt import Burnt
from services.closed_eyes_result import eye_closed_score
from services.image_io import safe_imread

# משקולות לציון הסופי (באחוזים)
SHARPNESS_WEIGHT = 0.55
BURNT_WEIGHT = 0.10
CLOSED_EYES_WEIGHT = 0.35

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

class DeduplicateService:
    """שירות לאיתור והסרת תמונות כפולות מתוך תיקיית אירוע"""

    @staticmethod
    def _compute_quality_score(image_path: str) -> float:
        """
        מחשב ציון איכות סופי באחוזים [0, 1] לפי:
        - 55% חדות (Sharpness)
        - 10% שרוף/חשוף יתר (Burnt)
        - 35% עיניים פקוחות (Closed Eyes)
        """
        img = safe_imread(image_path)
        if img is None:
            return 0.0

        sharpness_score = Sharpness.calculate_sharpness_laplacian(image=img)
        burnt_val = Burnt.burnt_score(image=img)
        eyes_score = eye_closed_score(img)

        # נרמול sharpness — ערך טיפוסי 0–3000, אבל יכול להיות גבוה בהרבה
        # clamp ל-1.0 בטווח הסביר
        sharpness_norm = min(sharpness_score / 1000.0, 1.0)

        final = (
            SHARPNESS_WEIGHT * sharpness_norm
            + BURNT_WEIGHT * burnt_val
            + CLOSED_EYES_WEIGHT * eyes_score
        )
        return round(final, 4)

    @staticmethod
    def remove_duplicate_images(
        folder_path: str,
        hash_threshold: int = 5,
        prefix_len: int = 8,
    ) -> dict:
        """
        סורק את תיקיית התמונות, מאתר כפילויות באמצעות perceptual hash,
        מעביר את הכפולות הפחות טובות לתיקיית Junk, ומשאיר רק את התמונה
        בעלת ציון האיכות הגבוה ביותר מכל קבוצה.

        Args:
            folder_path: נתיב לתיקיית התמונות
            hash_threshold: מרחק המינג המקסימלי בין hashes כדי להיחשב כפולות
            prefix_len: אורך הקידומת לקיבוץ ראשוני

        Returns:
            dict: סיכום — כמה תמונות הועברו ל-Junk, כמה נותרו
        """
        if not os.path.isdir(folder_path):
            raise ValueError(f"תיקייה לא נמצאה: {folder_path}")

        junk_folder = os.path.join(folder_path, "Junk")
        os.makedirs(junk_folder, exist_ok=True)

        # שלב 1 — קיבוץ תמונות לפי perceptual hash
        buckets: dict[str, list[dict]] = defaultdict(list)

        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(SUPPORTED_FORMATS):
                continue

            path = os.path.join(folder_path, filename)
            try:
                img = Image.open(path).convert("RGB")
                h = imagehash.phash(img)
            except Exception:
                continue

            bucket_key = str(h)[:prefix_len]
            buckets[bucket_key].append({
                "filename": filename,
                "path": path,
                "hash": h,
            })

        moved_count = 0
        kept_count = 0

        # שלב 2 — בתוך כל דלי, קבץ לפי דמיון אמיתי (המינג ≤ threshold)
        for bucket in buckets.values():
            groups: list[list[dict]] = []

            for item in bucket:
                found_group = None
                for group in groups:
                    if abs(item["hash"] - group[0]["hash"]) <= hash_threshold:
                        found_group = group
                        break

                if found_group is not None:
                    found_group.append(item)
                else:
                    groups.append([item])

            # שלב 3 — מכל קבוצה: חשב ציון איכות, השאר את הטוב ביותר, העבר את השאר ל-Junk
            for group in groups:
                if len(group) == 1:
                    kept_count += 1
                    continue

                # חשב ציון איכות לכל תמונה בקבוצה
                for item in group:
                    item["score"] = DeduplicateService._compute_quality_score(
                        item["path"]
                    )

                # מיון לפי ציון יורד — הראשון הוא הטוב ביותר
                group.sort(key=lambda x: x["score"], reverse=True)

                best = group[0]
                kept_count += 1

                # העבר את הכפולות הפחות טובות ל-Junk
                for dup in group[1:]:
                    dest = os.path.join(junk_folder, dup["filename"])
                    # טפל בהתנגשות שמות
                    if os.path.exists(dest):
                        base, ext = os.path.splitext(dup["filename"])
                        dest = os.path.join(junk_folder, f"{base}_dup{ext}")
                    shutil.move(dup["path"], dest)
                    moved_count += 1

        return {
            "status": "ok",
            "folder": folder_path,
            "junk_folder": junk_folder,
            "moved_to_junk": moved_count,
            "kept": kept_count,
            "total_processed": moved_count + kept_count,
        }


