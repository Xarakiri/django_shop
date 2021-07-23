from django.db import models

#**************
#1 Category
#2 Product
#3 CartProduct
#4 Cart
#5 Order
#**************
#6 Customer
#7 Specification


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name