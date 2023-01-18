from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('<int:pk>', views.ProductDetailsAPIView.as_view(), name='product-details'),
    path('', views.ProductListCreateAPIView.as_view()),
    path('products/', views.ProductListCreateAPIViewSet.as_view({'get': 'list', 'post': 'create'}))
]
