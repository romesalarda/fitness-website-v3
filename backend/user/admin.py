from django.contrib import admin

from user.models import PersonalBest, User

# Register your models here.

admin.site.register(User)
admin.site.register(PersonalBest)