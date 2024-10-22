from django.db import models
from django.contrib.auth.models import User

class SavedStock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stock_symbol = models.CharField(max_length=10)  # Stock ticker symbol
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.stock_symbol
