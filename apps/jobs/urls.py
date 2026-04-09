from rest_framework.routers import DefaultRouter
from .views import JobOfferViewSet, PublicJobOfferViewSet

router = DefaultRouter()
router.register(r"", JobOfferViewSet, basename="jobs")
router.register(r"public", PublicJobOfferViewSet, basename="public-jobs")

urlpatterns = router.urls