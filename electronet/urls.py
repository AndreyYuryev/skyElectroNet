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
from electronet.views import ProductViewSet, CompanyViewSet

app_name = ElectronetConfig.name

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')
router.register(r'company', CompanyViewSet, basename='company')
# router.register(r'deliveries', DeliveriesViewSet, basename='deliveries')

urlpatterns = [
    # path('api/v1/public/', PublicHabitListAPIView.as_view(), name='public-list'),
    path('api/v1/', include(router.urls)),
]
