from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name',
                  'age', 'phone')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name']




class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductListSerializer(serializers.ModelSerializer):
    product_image= ProductImageSerializer(many=True,read_only=True)
    created_date = serializers.DateField(format='%d-%m-%y')
    count_people = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id','product_name','price','product_type','product_images','product_image','created_date', 'count_people', 'average_rating']

    def get_count_people(self, obj):
        return obj.get_count_people()

    def get_average_rating(self, obj):
        return obj.get_average_rating()


class SubCategoryDetailSerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True,read_only=True)
    class Meta:
        model = SubCategory
        fields =['subcategory_name','products']


class SupCategorySerializer(serializers.ModelSerializer):
    category = CategoryListSerializer(many=True,read_only=True)
    class Meta:
        model =SubCategory
        fields = ['category']


class SubCategoryNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['subcategory_name']



class ReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateField(format='%d-%m-%y')
    user = UserProfileSimpleSerializer()
    class Meta:
        model = Review
        fields = ['user','stars','comment','created_date']



class ProductDetailSerializer(serializers.ModelSerializer):
    sub_categories = SupCategorySerializer(many=True,read_only=True)
    product_images = ProductImageSerializer(many=True,read_only=True)
    created_date = serializers.DateField(format='%d-%m-%y')
    # cubcategory = SubCategoryDetailSerializer()
    reviews = ReviewSerializer(many=True,read_only=True)


    class Meta:
        model = Product
        fields = ['product_name', 'price',  'sub_categories','product_images','video',
                  'article_number','description','product_type','created_date', 'subcategory', 'reviews']


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductDetailSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only = True,
                                                    source='product')

    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields =['id','product','product_id','quantity','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields =['id','user','items','total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


