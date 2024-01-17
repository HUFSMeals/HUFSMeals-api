from django.db import models
from accounts.models import User
from restaurant.models import Restaurant
import uuid
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile

def review_image_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return f'review_image/{instance.review.pk}/{filename}'


class Review(models.Model):
    """
    리뷰 model
    """
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE, related_name = 'review')
    restaurant = models.ForeignKey(Restaurant, null = True, on_delete = models.CASCADE, related_name = 'review')
    title = models.CharField(max_length = 100)
    body = models.TextField(default = "")
    src_lang = models.CharField(max_length = 10, null = True) # 작성된 리뷰의 언어
    created_at = models.DateField(auto_now_add = True, null = True)
    score = models.IntegerField(default= 0)
    
    def __str__(self):
        return self.title
    

class ReviewImage(models.Model):
    """
    리뷰 사진 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE, related_name = 'image')
    review_image = models.ImageField(upload_to = review_image_path, null = True, blank = True) # 원본 이미지


class TranslatedReview(models.Model):
    """
    번역된 리뷰 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE, related_name = 'translated_review')
    src_lang = models.CharField(max_length = 10, null = True) # 번역된 언어
    body = models.TextField(default = "")