from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import *
from .models import *
from rest_framework import viewsets,generics, status
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter,OrderingFilter
from .pagination import CategoryPagination, ProductPagination
from .filters import ProductFilter
from rest_framework.response import Response

class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)



class CategoryListAPIView(generics.ListAPIView):
    queryset =Category.objects.all()
    serializer_class = CategoryListSerializer



class SubCategoryListAPIVew(generics.ListAPIView):
    queryset =SubCategory.objects.all()
    serializer_class = SupCategorySerializer



class SubCategoryDetailAPIView(generics.RetrieveAPIView):
    queryset =SubCategory.objects.all()
    serializer_class = SupCategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset =Product.objects.all()
    serializer_class = ProductDetailSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    filterset_fields = ['product_type','price']
    ordering_fields = ['price','created_date']
    pagination_class = ProductPagination


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset =ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductListAPIVew(generics.ListAPIView):
    queryset =Product.objects.all()
    serializer_class =ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter,OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    filterset_fields = ['product_type','price']
    ordering_fields = ['price','created_date']
    pagination_class = ProductPagination



class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset =ProductImage.objects.all()
    serializer_class =ProductDetailSerializer



class ReviewViewSet(viewsets.ModelViewSet):
    queryset =Review.objects.all()
    serializer_class =ReviewSerializer


class CartViewSet(generics.RetrieveAPIView):
    serializer_class = CartSerializer


    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)



    def retrieve(self, request, *args, **kwargs):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer


    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart,created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

