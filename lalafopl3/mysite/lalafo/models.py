from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)


    def __str__(self):
        return self.category_name


class Product(models.Model):
      product_name = models.CharField(max_length=100, unique=True)
      price = models.PositiveIntegerField()
      phone_number= PhoneNumberField()
      description = models.TextField()
      product_type = models.BooleanField()
      create_date = models.DateTimeField(auto_now_add=True)
      image = models.ImageField(null=True, blank=True)

      def __str__(self):
          return self.product_name