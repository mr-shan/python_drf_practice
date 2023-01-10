from django.urls import path

from . import views

urlpatterns = [
    path('<int:pk>', views.ProductDetailsAPIView.as_view()),
    path('', views.ProductListCreateAPIView.as_view()),
    path('products/', views.ProductListCreateAPIViewSet.as_view({'get': 'list', 'post': 'create'}))
    # path('apple-products', views.AppleProductListModelMixin.as_view())
    # path('', views.index),
]
