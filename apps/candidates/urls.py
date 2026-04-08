from rest_framework.routers import DefaultRouter
from .views import CandidateProfileViewSet

router = DefaultRouter()
router.register(r"", CandidateProfileViewSet, basename="candidates")

urlpatterns = router.urls