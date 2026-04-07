from django.urls import path
from .views import GetHealth

urlpatterns = [
    path(
        "health",
        GetHealth.as_view(),
        name="get_health"
    )
]