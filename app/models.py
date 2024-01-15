from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# Create your models here.
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1','password2']

#category
class Category(models.Model):
    sub_category = models.ForeignKey('self', on_delete=models.CASCADE, related_name="cateories", null=True, blank=True)
    is_sub = models.BooleanField(default=False)
    name = models.CharField(max_length=200, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    def __str__(self) :
        return self.name
class Product(models.Model):
    category =  models.ManyToManyField(Category, related_name='product')
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

    def get_cart_items(self):
        return self.cartitem_set.all()
    def get_cart_total(self):
        cart_items = self.get_cart_items()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        return total_price
    def get_total_items(self):
        cart_items = self.get_cart_items()
        total_items = sum(item.quantity for item in cart_items)
        return total_items

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    
    @property 
    def get_price(self):
        price = self.product.price*self.quantity
        return price
