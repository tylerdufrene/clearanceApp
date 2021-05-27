from django.db import models
from django.utils import timezone

# Create your models here.



class Products(models.Model):
    id = models.AutoField(db_column='product_id', primary_key=True, auto_created=True)
    brand = models.CharField(max_length=300, default=None, db_column='brand')
    product_name = models.CharField(max_length=500, db_column='product_name')
    old_price = models.DecimalField(decimal_places=2, max_digits=6, db_column='old_price')
    new_price = models.DecimalField(decimal_places=2, max_digits=6,  db_column='new_price')
    image = models.CharField(max_length=5000, db_column='IMAGE')
    link = models.CharField(max_length=500, db_column='link')
    discount = models.DecimalField(decimal_places=2, max_digits=5, db_column='discount', default=None)
    sizes = models.CharField(max_length=250, db_column='sizes', default=None)
    colors = models.CharField(max_length=5000, db_column='colors', default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.product_name
    
    
