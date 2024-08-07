from django.db import models

# Create your models here.
class Notice(models.Model):
    title =  models.CharField(max_length = 100)
    body = models.TextField(null = False)
    created_at = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'notice'