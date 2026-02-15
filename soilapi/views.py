from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ultralytics import YOLO
from PIL import Image
import io
import os
from django.conf import settings
from .crop_recommendation import recommend_crops



# Load model ONCE (important for performance)
SOIL_CHECK_MODEL = YOLO(
    os.path.join(settings.BASE_DIR, "models", "soil_vs_nonsoil.pt")
)

SOIL_TYPE_MODEL = YOLO(
    os.path.join(settings.BASE_DIR, "models", "soil_type.pt")
)



class SoilRecognitionAPIView(APIView):

    def post(self, request):
        image_file = request.FILES.get("image")

        if not image_file:
            return Response(
                {"error": "Image is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            image = Image.open(image_file).convert("RGB")

            # -------------------------
            # STEP 1: Soil / Non-Soil
            # -------------------------
            soil_check = SOIL_CHECK_MODEL.predict(image, verbose=False)[0]
            probs1 = soil_check.probs

            label1 = SOIL_CHECK_MODEL.names[probs1.top1]
            conf1 = float(probs1.top1conf)

            if label1 == "non_soil":
                return Response({
                    "soil_detected": False,
                    "message": "Uploaded image is not soil",
                    "confidence": round(conf1, 4)
                }, status=status.HTTP_200_OK)

            # -------------------------
            # STEP 2: Soil Type
            # -------------------------
            soil_type_result = SOIL_TYPE_MODEL.predict(image, verbose=False)[0]
            probs2 = soil_type_result.probs

            soil_label = SOIL_TYPE_MODEL.names[probs2.top1]
            soil_conf = float(probs2.top1conf)

            # -------------------------
            # STEP 3: Crop Recommendation
            # -------------------------
            crops = recommend_crops(soil_label)

            return Response({
                "soil_detected": True,
                "soil_type": soil_label,
                "confidence": round(soil_conf, 4),
                "recommended_crops": crops
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
