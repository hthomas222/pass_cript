# vault/forms.py
from django import forms
from .models import VaultEntry


class VaultEntryForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "autocomplete": "new-password",
            }
        ),
        label="Plaintext Passphrase",
    )

    class Meta:
        model = VaultEntry
        fields = ["website_name", "website_url", "username_or_email"]