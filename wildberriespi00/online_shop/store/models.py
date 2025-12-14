from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(validators=[MinValueValidator(18), MaxValueValidator(65)],
                                      null=True,blank=True)
    phone = PhoneNumberField(null=True,blank=True)
    avatar = models.ImageField(upload_to='user_images',null=True,blank=True)
    StatusChoices = (
    ('gold', 'Gold'),#75%
    ('silver', 'silver'),#50%
    ('bronze', 'bronze'),#25%
    ('simple', 'simple'))#0
    status = models.CharField( max_length=20,choices=StatusChoices,default='simple')
    date_registered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} {self.last_name}'



class Category(models.Model):
    category_image = models.ImageField(upload_to='category_photo')
    category_name = models.CharField(max_length=30,unique=True)


    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=30,unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='sub_categories')


    def __str__(self):
        return self.subcategory_name


class Product(models.Model):
    subcategory = models.ForeignKey(SubCategory,on_delete=models.CASCADE,related_name='products')
    product_name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    article_number = models.PositiveIntegerField(unique=True,verbose_name='Артикул')
    description = models.TextField()
    video = models.FileField(upload_to='product_video',null=True,blank=True)
    product_type = models.BooleanField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.product_name

    def get_average_rating(self):
        review = self.reviews_product.all()
        if review.exists():
            return round(sum(i.stars for i in review) / review.count(), 2)
        return 0

    def get_count_people(self):
        return self.reviews_product.count()



class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='product_photo/')


    def __str__(self):
        return f'{self.product} {self.image}'




class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE, related_name='reviews_product')
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='reviews')
    stars = models.PositiveSmallIntegerField(choices=[(i,str(i)) for i in range(1,6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.user}, {self.product}, {self.stars}'



class Cart(models.Model):
    user = models.OneToOneField(UserProfile,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'


    def get_total_price(self):
        return sum([i.get_total_price() for i in self.items.all()])



class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f'{self.product} {self.quantity}'


    def get_total_price(self):
        return self.quantity * self.product.price








