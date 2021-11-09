from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	slug = models.SlugField(max_length=50, blank=True, null=True)
	image = models.ImageField(upload_to="category/",blank=True,null=True)
	service = models.BooleanField(default=False)


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('products', kwargs={'cat': self.slug})



class Product(models.Model):
	name = models.CharField(max_length=500, db_index=True)
	slug = models.SlugField(max_length=50, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="category",null=True)
	alter_category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
	article = models.CharField(max_length=20, null=True)
	price = models.FloatField(default=0.0)
	dsc = models.TextField(null=True, blank=True)
	stats= models.JSONField(blank=True,null=True)
	img = models.ImageField(upload_to="products/", blank=True,null=True)
	in_storage = models.BooleanField(default=True)
	is_new = models.BooleanField(default=False)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		if self.category is None:
			return reverse('product_detail', kwargs={'cat': self.alter_category.slug,"pk":self.id})
		else:
			return reverse('product_detail', kwargs={'cat': self.category.slug,"pk":self.id})


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Delivery(models.Model):
	name = models.CharField(max_length=70)
	image = models.ImageField(upload_to="delivery/",blank=True,null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Доставка'
		verbose_name_plural = 'Доставка'


class Payment(models.Model):
	name = models.CharField(max_length=70)
	image = models.ImageField(upload_to="payment/",blank=True,null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Оплата'
		verbose_name_plural = 'Оплата'

class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # total price for all products in order
    customer_name = models.CharField(max_length=64, blank=True, null=True, default=None)
    customer_email = models.EmailField(blank=True, null=True, default=None)
    customer_phone = models.CharField(max_length=48, blank=True, null=True, default=None)
    customer_address = models.CharField(max_length=128, blank=True, null=True, default=None)
    delivery = models.ForeignKey(Delivery,on_delete=models.CASCADE, blank=True, null=True, default=None)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, blank=True, null=True, default=None)
    confirm = models.CharField(max_length=50, blank=True, null=True, default=None)
    cancel = models.TextField(blank=True, null=True, default=None)
    comments = models.TextField(blank=True, null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    def get_absolute_url(self):
        return reverse("order_detail",kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None,related_name="p2o", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item
        super(ProductInOrder, self).save(*args, **kwargs)


# @disable_for_loaddata
def product_in_order_post_save(sender, instance, created, **kwargs):
    order = instance.order
    all_products_in_order = ProductInOrder.objects.filter(order=order, is_active=True)

    order_total_price = 0
    for item in all_products_in_order:
        order_total_price += item.total_price

    instance.order.total_price = order_total_price
    instance.order.save(force_update=True)


post_save.connect(product_in_order_post_save, sender=ProductInOrder)

class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, null=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.DO_NOTHING)
    nmb = models.IntegerField(default=1)
    price_per_item = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # price*nmb
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        price_per_item = self.product.price
        self.price_per_item = price_per_item
        self.total_price = int(self.nmb) * price_per_item
        super(ProductInBasket, self).save(*args, **kwargs)


class Market(models.Model):
    point = models.CharField(max_length=100, blank=True, null=True, default=None)
    address = models.CharField(max_length=200)
    
    def __str__(self):
        return self.address

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class News(models.Model):
    title = models.CharField(max_length=150, null=True)
    slug = models.SlugField(max_length=150)
    body = models.TextField()
    publicate = models.DateField(auto_now_add=True, auto_now=False, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = 'Новости'


class Document(models.Model):
    name = models.CharField(max_length=150)
    file = models.FileField()