from django.db import models
import uuid

# Create your models here.
def restaurant_images_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'restaurant_images/{filename}'

class Restaurant(models.Model):
    name = models.CharField(max_length = 50)
    restaurant_image = models.ImageField(upload_to = restaurant_images_path, blank = True, null = True)
    latitude = models.CharField(max_length = 20)
    longitude = models.CharField(max_length = 20)
    opening_hours = models.TextField(default = "")
    address = models.CharField(max_length = 200)
    category = models.CharField(max_length = 50)
    phone = models.CharField(max_length = 50)
    review_cnt = models.IntegerField(default = 0)
    score_accum = models.IntegerField(default = 0) # 누적 평점(평균 산출용)
    score_avg = models.DecimalField(max_digits = 2, decimal_places = 1, default = 0) # 평균 평점(소수 한 자리수까지)


def menu_images_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'menu_images/{instance.restaurant.name}_{instance.restaurant.pk}/{filename}'

class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name = 'menu')
    name = models.CharField(max_length = 50)
    menu_image = models.ImageField(upload_to = menu_images_path, blank = True, null = True)