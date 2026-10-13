# vault/models.py
from django.db import models
from django.contrib.auth.models import User

class VaultEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vault_entries")
    website_name = models.CharField(max_length=100)
    website_url = models.URLField(blank=True)
    username_or_email = models.CharField(max_length=150)
    encrypted_password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # <-- ADD THIS FIELD

    def __str__(self):
        return f"{self.website_name} ({self.username_or_email})"