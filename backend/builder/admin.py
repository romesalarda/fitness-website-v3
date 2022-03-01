from django.contrib import admin

from builder.models import Category, Exercise, Superset, Workout

# Register your models here.
admin.site.register(Workout)
admin.site.register(Exercise)
admin.site.register(Superset)
admin.site.register(Category)
