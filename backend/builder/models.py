from django.conf import settings
from django.utils import timezone
from django.db import models
from django.template.defaultfilters import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Category(models.Model):
    '''
    Category to add extra detail about what parts of the body the exercise targets
    '''
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, blank=True)
    description = models.TextField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs) 


class Exercise(models.Model):
    '''
    A workout exercise that contains sets and repetitions
    '''
    # id related info
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="exercises", blank=True, null=True)
    # workout related info
    sets = models.IntegerField(default=4, validators=[MinValueValidator(0), MaxValueValidator(12)])
    repetitions = models.IntegerField(default=12, validators=[MinValueValidator(0), MaxValueValidator(500)])
    duration = models.FloatField(default=0, blank=True)
    rest_period = models.FloatField(default=0, blank=True, validators=[MinValueValidator(0), MaxValueValidator(999)])

    # determine direction of push or pull
    class Direction(models.TextChoices):
        HORIZONTAL = "1", "HORIZONTAL"
        VERTICAL = "2", "VERTICAL"
    direction = models.CharField(max_length=2, choices=Direction.choices, blank=True, null=True)
    # determine what area of the body we are targeting
    class Target(models.TextChoices):
        LOWER = "1", "LOWER"
        UPPER = "2", "UPPER"
        CORE = "3", "CORE"
    target = models.CharField(max_length=2, choices=Target.choices, blank=True, null=True)
    # what level the exercise is
    class Level(models.TextChoices):
        BEGINNER = "1", "BEGINNER"
        INTERMEDIATE = "2", "INTERMEDIATE"
        ADVANCE = "3", "ADVANCE"
    level = models.CharField(max_length=2, choices=Level.choices, blank=True, null=True)

    categories = models.ManyToManyField(Category, related_name="exercises", blank=True)
    # extra data
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=300, null=True, blank=True)

    # defines if a exercise is global for user workouts to use
    public = models.BooleanField(default=False) 
    # defines if an execise is only allowed to be copied
    copy_only = models.BooleanField(default=False)
    preset = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.preset:
            # if the exercise is a preset, only allow users to copy the exercise
            # to avoid global updates for other users
            self.public = True
            self.copy_only = True
        super(Exercise, self).save(*args, **kwargs) 


class Superset(models.Model):
    '''
    A superset consists of multiple exercises that have no rest periods in between
    '''
    # id related data
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="supersets", blank=True, null=True)
    # meta related data
    created = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=300, null=True, blank=True)
    # relation data
    exercises = models.ManyToManyField(Exercise, related_name="supersets", blank=True)
    categories = models.ManyToManyField(Category, related_name="supersets", blank=True)

    # defines if a supertset is global for user workouts to use
    public = models.BooleanField(default=False) 
    # defines if a superset is only allowed to be copied
    copy_only = models.BooleanField(default=False)
    preset = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "supersets"
        ordering = ["-title"]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        if self.preset:
            # if the superset is a preset, only allow users to copy the superset
            # to avoid global updates for other users
            self.public = True
            self.copy_only = True
        super(Superset, self).save(*args, **kwargs) 

class Workout(models.Model):
    '''
    Top level model for the builder. Can create relations to multiple exercises and multiple supersets.
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=250, blank=True)

    description = models.TextField(max_length=300, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    last_updated = models.DateTimeField(default=timezone.now, null=True, blank=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="workouts")
    exercises = models.ManyToManyField(Exercise, related_name="workouts", blank=True)
    supersets = models.ManyToManyField(Superset, related_name="workouts", blank=True)
    
    class Meta:
        ordering = ["-created"]

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.last_updated = timezone.now()
        super(Workout, self).save(*args, **kwargs) 

    def __str__(self) -> str:
        return self.title 


    