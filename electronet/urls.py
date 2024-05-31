"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from electronet.apps import ElectronetConfig
from rest_framework.routers import DefaultRouter
from electronet.views import (DebtViewSet, DeliveryAPIView,
                              ProductListAPIView, ProductCreateAPIView, ProductRetriveUpdateAPIView, \
                              CompanyListAPIView, CompanyCreateAPIView, CompanyRetriveUpdateAPIView,
                              DeliveryNetListAPIView, DeliveryNetCreateAPIView, DeliveryNetRetriveUpdateAPIView)

app_name = ElectronetConfig.name

router = DefaultRouter()
# router.register(r'product', ProductViewSet, basename='product')
# router.register(r'company', CompanyViewSet, basename='company')
router.register(r'debt', DebtViewSet, basename='debt')
# router.register(r'deliverynet', DeliveryNetViewSet, basename='deliverynet')

urlpatterns = [
    path('api/v1/product/', ProductListAPIView.as_view(), name='product-list'),
    path('api/v1/product/create/', ProductCreateAPIView.as_view(), name='product-create'),
    path('api/v1/product/<int:pk>/', ProductRetriveUpdateAPIView.as_view(), name='product-retrive-update'),
    path('api/v1/company/', CompanyListAPIView.as_view(), name='company-list'),
    path('api/v1/company/create/', CompanyCreateAPIView.as_view(), name='company-create'),
    path('api/v1/company/<int:pk>/', CompanyRetriveUpdateAPIView.as_view(), name='company-retrive-update'),
    path('api/v1/delivery/', DeliveryAPIView.as_view(), name='delivery'),
    path('api/v1/deliverynet/', DeliveryNetListAPIView.as_view(), name='deliverynet-list'),
    path('api/v1/deliverynet/create/', DeliveryNetCreateAPIView.as_view(), name='deliverynet-create'),
    path('api/v1/deliverynet/<int:pk>/', DeliveryNetRetriveUpdateAPIView.as_view(), name='deliverynet-retrive-update'),
    path('api/v1/', include(router.urls)),
]
