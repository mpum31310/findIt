from django.db import models
from accounts.models import User


class Child(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='children')
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    grade = models.CharField(max_length=50)
    school = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} {self.surname}"

