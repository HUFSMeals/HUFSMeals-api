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
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE, related_name = 'review')
    restaurant = models.ForeignKey(Restaurant, null = True, on_delete = models.CASCADE, related_name = 'review')
    title = models.CharField(max_length = 100, default = "")
    body = models.TextField(default = "")
    src_lang = models.CharField(max_length = 10, null = True, default = "") # 작성된 리뷰의 언어
    created_at = models.DateField(auto_now_add = True, null = True)
    score = models.IntegerField(default= 0)
    
    def __str__(self):
        return f"{self.user}_{self.restaurant}_{self.title}"

    class Meta:
        db_table = 'review'
    

class ReviewImage(models.Model):
    """
    리뷰 사진 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE, related_name = 'review_image')
    review_image = models.ImageField(upload_to = review_image_path, null = True, blank = True) # 원본 이미지

    def __str__(self):
        return f"{self.review.user}_{self.review.restaurant}_{self.pk}"

    class Meta:
        db_table = 'review_image'


class TranslatedReview(models.Model):
    """
    번역된 리뷰 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE, related_name = 'translated_review')
    src_lang = models.CharField(max_length = 10, null = True, default = "") # 번역된 언어
    body = models.TextField(default = "")

    def __str__(self):
        return f"{self.review.user}_{self.review.restaurant}_{self.src_lang}"

    class Meta:
        db_table = 'translated_review'