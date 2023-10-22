from django.db import models
from django.contrib.auth.models import User
CATEGORY = (
    ('Statonary', 'Stationary',),
    ('Electronics', 'Electronics',),
   
)
class Product(models.Model):
     name = models.CharField(max_length = 100 , null=True)
     category = models.CharField(max_length = 20,choices = CATEGORY ,null=True)
     quantity = models.PositiveBigIntegerField( null=True)
     
     
     class Meta:
         verbose_name_plural = 'Product'
     
     
     def __str__(self):
         return f'{self.name}-{self.quantity}'

class  File(models.Model):
    file = models.FileField(upload_to = 'files') 
        
     
class Order(models.Model):
     product = models.ForeignKey(Product,on_delete=models.CASCADE, null = True)
     staff = models.ForeignKey(User,models.CASCADE, null = True)
     order_quantity = models.PositiveBigIntegerField(null=True)
     date  = models.DateTimeField(auto_now_add=True)
     
     class Meta:
         verbose_name_plural = 'Order'
     
     def __str__(self):
         return f'{self.product} ordered By {self.staff.username}'
     
     
     