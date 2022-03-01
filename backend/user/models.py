from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.utils import timezone
from django.template.defaultfilters import slugify

import uuid

class CustomUserManager(BaseUserManager):
    # Custom user model manager where email is the unique identifiers
    # for authentication instead of usernames.
   
    def create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.
    
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    '''
    Custom user model
    '''
    username = models.CharField(max_length=20)
    email = models.EmailField(_('email address'), unique=True)

    description = models.TextField(max_length=300, blank=True, null=True)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    
    weight = models.FloatField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class PersonalBest(models.Model):
    '''
    Represents a user's personal best for an exercise
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="personal_bests")

    description = models.TextField(max_length=400, null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    repetitions = models.IntegerField(null=True, blank=True)

    joined = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        self.slug = slugify(self.title)
        super(PersonalBest, self).save(args, kwargs)

class Target(models.Model):
    '''
    Represents a goal that the user may want to pursue
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="goals")

    description = models.TextField(max_length=400, null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    repetitions = models.IntegerField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)
    
    target_date = models.DateField(null=True, blank=True)

    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.last_updated = timezone.now()
        self.slug = slugify(self.title)
        super(PersonalBest, self).save(args, kwargs)
