from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# 현업에서는 로컬에 저장하는 FileSystemStorage 방식을 쓰지 않고, AWS의 S3를 사용한다고 합니다.
# 하지만 AWS 특성 상 비용이 발생하니 논의 후에 추후 변경할지 정해보아요
fs = FileSystemStorage(location='/media/menu')


# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    opening_hours = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    review_cnt = models.IntegerField(default=0)
    sorce_avg = models.FloatField(default=0.0)


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu')
    name = models.CharField(max_length=50)
    image = models.ImageField(storage=fs)

    def __str__(self):
        return self.name