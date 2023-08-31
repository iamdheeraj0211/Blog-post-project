from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# user=get_user_model()
class PostModel(models.Model):
    title=models.CharField(max_length=100)
    body=models.TextField()
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    # author=models.CharField(max_length=45)
    # def save(self, *args, **kwargs):
    #     if not self.author_id:
    #         if hasattr(self, 'user'):
    #             self.author = self.user 
    #     super().save(*args, **kwargs)