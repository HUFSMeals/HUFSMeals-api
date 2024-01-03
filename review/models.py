from django.db import models
from accounts.models import User
from restaurant.models import Restaurant
import uuid

def review_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'review_image/{instance.review.pk}/{filename}'


class Review(models.Model):
    """
    리뷰 model
    """
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null = True, on_delete = models.CASCADE)
    title = models.CharField(max_length = 100)
    body = models.TextField(default = "")
    src_lang = models.CharField(max_length = 10, null = True)
    created_at = models.DateField(auto_now_add = True, null = True)
    score = models.IntegerField(default= 0)
    
    def __str__(self):
        return self.title
    

class ReviewImage(models.Model):
    """
    리뷰 사진 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE)
    review_image = models.ImageField(upload_to = review_image_path, blank = True)