from django.urls import path, include
from rest_framework.routers import DefaultRouter

from shop.products import views


router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename="product")


urlpatterns = [
    path('', include(router.urls)),
    path(
        'products/<int:pk>/image-upload',
        views.ImageUploadView.as_view(),
        name="image-upload"
    ),
]
