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
    user = models.ForeignKey(User, null = True, on_delete = models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, null = True, on_delete = models.CASCADE)
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
    review = models.ForeignKey(Review, on_delete = models.CASCADE)
    review_image = models.ImageField(upload_to = review_image_path, null = True, blank = True) # 축소된 이미지
    original_image = models.ImageField(upload_to = review_image_path, blank = True) # 원본 이미지

    def save(self, *args, **kwargs):
        if self.original_image:
            image = Image.open(self.original_image)

            # 축소할 기준 크기 설정
            base_size = (100, 100)  # 원하는 기준 크기로 설정

            # 이미지의 가로, 세로 크기를 가져옴
            width, height = image.size

            # 이미지의 가로 세로 비율 계산
            ratio = min(base_size[0] / width, base_size[1] / height)

            # 새로운 크기 계산
            new_size = (int(width * ratio), int(height * ratio))

            # 이미지를 새로운 크기로 조절하여 저장
            image.thumbnail(new_size)

            # 축소된 이미지 경로 설정
            if not self.review_image:
                self.review_image.name = review_image_path(self, self.original_image.name)

            # Save the review_image field
            image_thumb_io = BytesIO()
            cropped_image = image.convert('RGB')
            cropped_image.save(image_thumb_io, format='JPEG')
            image_thumb = SimpleUploadedFile(
                name=f'{self.original_image.name.split(".")[0]}_thumb.jpg',
                content=image_thumb_io.getvalue(),
                content_type='image/jpeg'
            )
            self.review_image.save(image_thumb.name, image_thumb, save=False)

        # Call the superclass save method
        super().save(*args, **kwargs)


class TranslatedReview(models.Model):
    """
    번역된 리뷰 model
    """
    review = models.ForeignKey(Review, on_delete = models.CASCADE)
    src_lang = models.CharField(max_length = 10, null = True) # 번역된 언어
    title = models.CharField(max_length = 100)
    body = models.TextField(default = "")