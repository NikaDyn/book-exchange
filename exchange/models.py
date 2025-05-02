from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    category = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ExchangeOffer(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_sent')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='offers_received')
    offered_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='offered_in')
    requested_book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='requested_in')
    status = models.CharField(max_length=20, choices=[('pending', 'Очікує'), ('accepted', 'Прийнято'), ('rejected', 'Відхилено')], default='pending')

    def __str__(self):
        return f"{self.offered_book} → {self.requested_book} ({self.status})"


class ExchangeRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    offered_book = models.ForeignKey(Book, related_name='offered_requests', on_delete=models.CASCADE)
    requested_book = models.ForeignKey(Book, related_name='requested_requests', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Очікує'), ('accepted', 'Прийнято'), ('rejected', 'Відхилено')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} → {self.to_user.username}"
