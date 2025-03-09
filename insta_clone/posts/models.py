from django.contrib.auth import get_user_model
from django.db import models

User  = get_user_model()


class Post(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='posts'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True, null=True
    )
    caption = models.TextField(
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.user} | {self.caption}"
    

class Like(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='likes'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ('user', 'post')


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, 
        related_name='comments'
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, 
        related_name='comments'
    )
    text = models.TextField(

    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
