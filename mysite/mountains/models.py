
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser, AnonymousUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from cart.models import Coupon

user_choices = [
    ("Newcomer", "Newcomer"),
    ("Regular user", "Regular user"),
    ("Top fan", "Top fan"),
    ("Manager", "Manager"),
    ("Blogger", "Blogger")
]

class AdvUser(AbstractUser):
    status = models.CharField(max_length=20, choices=user_choices, default='Newcomer', verbose_name='User status')
    phone = models.CharField(max_length=20, blank=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d', blank=True, null=True)

    def save(self, *args, **kwargs):
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username



# ----------------------------------------------------------------------------------------------------------------------

equipment_choices = [
    ('None', 'Choose:'),
    ("Available", "Available"),
    ("Do dyspozycji", "Do dyspozycji"),
    ("On order", "On order"),
    ("Na zamówienie", "Na zamówienie"),
    ("On sale soon", "On sale soon"),
    ("Wkrotce na wyprzedazy", "Wkrotce na wyprzedazy")
]
class Equipment(models.Model):
    title = models.CharField(verbose_name=_('Title'), max_length=50)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name=_('Brand'))
    available = models.CharField(verbose_name=_('Available'), choices=equipment_choices, max_length=50)
    price = models.DecimalField(verbose_name=_('Price'), max_digits=10, decimal_places=2)
    remainder = models.PositiveIntegerField(verbose_name=_('Remainder'))
    description = models.TextField(verbose_name=_('Description'), blank=True)
    subcategory = models.ForeignKey('Subcategory', on_delete=models.CASCADE, verbose_name=_('Subcategory'))
    image = models.ImageField(upload_to='equipment/%Y/%m/%d')
    comments = models.ManyToManyField('Comment', blank=True, verbose_name=_('Comments'))
    characteristic = models.ForeignKey('Characteristic', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_('Characteristics'))
    discount = models.DecimalField(verbose_name=_('Discount'), max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mountains:detail_equipment', args=[self.pk])

    @property
    def get_discount(self):
        self.price = self.price - self.price / 100 * self.discount
        return self.price

    class Meta:
        ordering = ['subcategory', 'price']







# ----------------------------------------------------------------------------------------------------------------------


class EquipmentStatistic(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.equipment.title

# ----------------------------------------------------------------------------------------------------------------------


class Wishes(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, null=True, blank=True)
    equipments = models.ManyToManyField(Equipment, blank=True)

# ----------------------------------------------------------------------------------------------------------------------


char_choices =[
    ("Men", "Men"),
    ("Mężczyźni", "Mężczyźni"),
    ("Kobiety", "Kobiety"),
    ("Woman", "Woman"),
    ("Unisex", "Unisex"),
    ("Dla obu płci", "Dla obu płci"),
    ("Child", "Child"),
    ("Dziecko", "Dziecko"),
]

level_choices = [
    ("Newbie", "Newbie"),
    ("Początkowy", "Początkowy"),
    ("Middle", "Middle"),
    ("Środkowy", "Środkowy"),
    ('Professional', "Professional"),
    ('Profesjonalny', "Profesjonalny"),
]

class Characteristic(models.Model):
    appointment = models.CharField(max_length=20, choices=char_choices, blank=True)
    level = models.CharField(max_length=20, choices=level_choices, blank=True)


# ----------------------------------------------------------------------------------------------------------------------


class Category(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('all_categories', args=[self.pk])



class Subcategory(models.Model):
    title = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('subcategories', args=[self.pk])


# ----------------------------------------------------------------------------------------------------------------------


class Store(models.Model):
    title = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    city = models.ForeignKey('City', on_delete=models.CASCADE)
    count_equipment = models.PositiveIntegerField(null=True, blank=True)
    equipments = models.ManyToManyField(Equipment)
    work_schedule = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['city']


# ----------------------------------------------------------------------------------------------------------------------


class City(models.Model):
    title = models.CharField(max_length=50)
    region = models.ForeignKey('Region', on_delete=models.CASCADE)


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['region', 'title']


# ----------------------------------------------------------------------------------------------------------------------


class Region(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title

#-----------------------------------------------------------------------------------------------------------------------


class Brand(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


# ----------------------------------------------------------------------------------------------------------------------

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE, related_name='blog_posts')
    short_description = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    comments = models.ManyToManyField('Comment', blank=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('mountains:post_details', args=[self.pk])


# ----------------------------------------------------------------------------------------------------------------------


class Comment(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now=True)
    text = models.TextField()

    class Meta:
        ordering = ['created_on']

# ----------------------------------------------------------------------------------------------------------------------


class Delivery(models.Model):
    delivery_option = models.CharField(max_length=50)
    payments = models.ManyToManyField('Payment')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.delivery_option


# ----------------------------------------------------------------------------------------------------------------------


class Payment(models.Model):
    payment = models.CharField(max_length=50)

    def __str__(self):
        return self.payment
