from django.urls import path

from products.api.views import ProductPriceAPIView

urlpatterns = [
    path('get-price/', ProductPriceAPIView.as_view())
]
