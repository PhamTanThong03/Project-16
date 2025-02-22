from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.forms import ModelForm
from product.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        if self.product:
            return self.product.title
        return "Product not set"

    @property
    def price(self):
        return self.product.price if self.product else 0

    @property
    def amount(self):
        return self.quantity * self.price

    @property
    def varamount(self):
        return self.quantity * self.price

    def countreview(self):
        reviews = ShopCart.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        return reviews.get("count", 0)


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']


class Order(models.Model):
    STATUS = (
        ('Mới', 'Mới'),
        ('Chấp nhận', 'Chấp nhận'),
        ('Đang chuẩn bị', 'Đang chuẩn bị'),
        ('Đang Ship', 'Đang Ship'),
        ('Hoàn Thành', 'Hoàn Thành'),
        ('Đã hủy', 'Đã hủy'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    total = models.FloatField()
    status = models.CharField(max_length=15, choices=STATUS, default='Mới')
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Order by {self.user.first_name} {self.user.last_name} - {self.code}"
        return f"Order by Unknown User - {self.code}"


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'phone', 'city', 'country']


class OrderProduct(models.Model):
    STATUS = (
        ('Mới', 'Mới'),
        ('Chấp Nhận', 'Chấp Nhận'),
        ('Đã hủy', 'Đã hủy'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    amount = models.FloatField()
    status = models.CharField(max_length=10, choices=STATUS, default='Mới')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.product:
            return self.product.title
        return "Product not set"
