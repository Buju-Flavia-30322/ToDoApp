from django.contrib import admin
from .models import TodoItem
from django.contrib.auth.models import User

admin.site.register(TodoItem)
# superuser admin, admin@admin.com, flavia12345
