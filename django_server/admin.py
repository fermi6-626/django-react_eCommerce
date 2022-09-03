from django.contrib import admin
from .models import Reset, Tokens, Users

# Register your models here.
admin.site.register(Users)
admin.site.register(Tokens)
admin.site.register(Reset)