from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(AbstractUser):
    """ 
    user model creates a user with the following fields:
    username: username of the user..username is unique and nullable
    user_type: student or lecturer
    full_name: full name of the user
    university_name: name of the university
    id_or_matricn_number: student id or matricn number
    """
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
    )
    
    username = models.CharField(max_length=80, unique=True, null=True, blank=True, error_messages={
        'unique': _("A user with that username already exists."),
    })
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    full_name = models.CharField(max_length=80)
    university_name = models.CharField(max_length=80)
    id_or_matricn_number = models.CharField(max_length=80, unique=True, error_messages={
        'unique': _("A user with that id already exists."),
    })

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('university_name', 'id_or_matricn_number')