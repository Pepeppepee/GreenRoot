from django.urls import path
from .views import SoilRecognitionAPIView

urlpatterns = [
    path("predict-soil/", SoilRecognitionAPIView.as_view(), name="predict_soil"),
]
