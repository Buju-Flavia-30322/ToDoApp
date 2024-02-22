from django.contrib.auth.models import User
from django.db import models

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
]


class TodoItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #  on_delete=models.CASCADE means that if a user is deleted, all associated TodoItems will also be deleted
    task = models.CharField(max_length=200)  # nume task
    description = models.TextField()  # descriere task
    status = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.task
