from django.db import models
from accounts.models import User
from items.models import Item


class Message(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='messages')
    sender_name = models.CharField(max_length=200)
    sender_email = models.EmailField(blank=True, null=True)
    sender_phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender_name} about {self.item.name}"

