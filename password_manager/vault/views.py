# vault/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import VaultEntryForm
from .models import VaultEntry
from .utils import decrypt_password, encrypt_password


@login_required
def dashboard(request):
    entries = VaultEntry.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "vault/dashboard.html", {"entries": entries})


@login_required
def add_password(request):
    if request.method == "POST":
        form = VaultEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user

            raw_pwd = form.cleaned_data["password"]
            entry.encrypted_password = encrypt_password(raw_pwd)

            entry.save()
            return redirect("dashboard")
    else:
        form = VaultEntryForm()

    return render(request, "vault/add_password.html", {"form": form})


@login_required
def edit_password(request, entry_id):
    """Update an existing credential entry."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)

    if request.method == "POST":
        form = VaultEntryForm(request.POST, instance=entry)
        if form.is_valid():
            updated_entry = form.save(commit=False)

            # Re-encrypt password if provided
            raw_pwd = form.cleaned_data["password"]
            updated_entry.encrypted_password = encrypt_password(raw_pwd)

            updated_entry.save()
            return redirect("dashboard")
    else:
        # Pre-fill decrypted password in form for editing
        try:
            initial_password = decrypt_password(entry.encrypted_password)
        except Exception:
            initial_password = ""

        form = VaultEntryForm(instance=entry, initial={"password": initial_password})

    return render(request, "vault/edit_password.html", {"form": form, "entry": entry})


@login_required
def delete_password(request, entry_id):
    """Delete a credential entry (POST only for security)."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)
    if request.method == "POST":
        entry.delete()
    return redirect("dashboard")


@login_required
def decrypt_api(request, entry_id):
    """AJAX endpoint for dashboard DECRYPT action."""
    entry = get_object_or_404(VaultEntry, id=entry_id, user=request.user)
    try:
        plain_text = decrypt_password(entry.encrypted_password)
        return JsonResponse({"password": plain_text})
    except Exception:
        return JsonResponse({"error": "DECRYPTION_FAILED"}, status=400)
