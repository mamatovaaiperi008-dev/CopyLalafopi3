from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'users', UserProfileViewSet)
# router.register(r'product', ProductViewSet)
router.register(r'images', ProductImageViewSet)
router.register(r'review', ReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view()),
    path('login', CustomLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('category', CategoryListAPIView.as_view(), name='category_list'),
    path('category/<int:pk>', CategoryListAPIView.as_view(), name='category_detail'),
    path('sub_category/', SubCategoryListAPIVew.as_view(), name='sub_category_list'),
    path('sub_category/<int:pk>', SubCategoryDetailAPIView.as_view(), name='sub_category_detail'),
    path('product/', ProductListAPIVew.as_view(), name='product_list'),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name='product_detail'),
    path('accounts/', include('allauth.urls')),
    path('cart/',CartViewSet.as_view(),name='cart_detail'),
    path('cart_items/',CartItemViewSet.as_view({'get': 'list','post':'create'})),
    path('cart_items/<int:pk>/',CartItemViewSet.as_view({'put':'update','delete':'destroy'})),
]
