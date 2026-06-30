import base64
import cv2
import numpy as np
# from services.face_utils import extract_single_faces
class FaceSelectedService:

    def base64_to_image(self, base64_str):

        if "base64," in base64_str:
            base64_str = base64_str.split("base64,")[1]

        base64_str += "=" * (-len(base64_str) % 4)

        img_data = base64.b64decode(base64_str)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        return img

    def process_selected_faces(self, bride_b64, groom_b64, faces_b64_list):

        bride = self.base64_to_image(bride_b64)
        groom = self.base64_to_image(groom_b64)

        faces = []
        for f in faces_b64_list:
            faces.append(self.base64_to_image(f))

        return {
            "status": "ok",
            "faces_count": len(faces)
        }
