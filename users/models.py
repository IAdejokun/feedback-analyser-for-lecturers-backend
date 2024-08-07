from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

# Create your models here.
    
class Universities(models.Model):
    """ 
    university model for creating & storing universities
    """
    name = models.CharField(max_length=80)
    
    def __str__(self):
        return self.name
    
class customUserManager(BaseUserManager):
    """ 
    custom user manager for creating users
    """
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError('Users must have a username')  
        user = self.model(username=username.strip(), **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)
    
    
class User(AbstractUser):
    """ 
    user model creates a user with the following fields:
    username: username of the user..username is unique and nullable
    user_type: student or lecturer
    full_name: full name of the user
    university: university of the user
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
    university = models.ForeignKey(Universities, on_delete=models.CASCADE, blank=True, null=True)
    id_or_matricn_number = models.CharField(max_length=80, unique=True, error_messages={
        'unique': _("A user with that id already exists."),
    })
    
    objects = customUserManager()

    def is_lecturer(self):
        return self.user_type == 'lecturer'
    
    def is_student(self):
        return self.user_type == 'student'

    def __str__(self):
        return f"{self.username} - {self.full_name}, ({self.get_user_type_display()})"
    class Meta:
        unique_together = ('university', 'id_or_matricn_number')
    
    
    
class Department(models.Model):
    """ 
    department model for creating & storing departments
    """
    
    name = models.CharField(max_length=80, unique=True)        

    def __str__(self):
        return self.name

class Course(models.Model):
    """ 
    course model for individual courses
    """
    
    title = models.CharField(max_length=80, unique=True)
    code = models.CharField(max_length=10, unique=True)
    lecturer = models.ForeignKey(User, related_name='lecturer_courses',limit_choices_to={'user_type': 'lecturer'},on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='student_courses',limit_choices_to={'user_type': 'student'})
    
    def __str__(self):
        return f"{self.code} {self.title}"
    
class Feedback_Survey(models.Model):    
    """ 
    feedback survey model for feedbacks
    """
    title = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='surveys')
    creator = models.ForeignKey(User, limit_choices_to={'user_type':'lecturer'}, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='surveys')

    def __str__(self):
        return f"{self.title} for {self.course}"

class Question(models.Model):
    """ 
    question model for feedback surveys
    """
    survey = models.ForeignKey(Feedback_Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(max_length=1000)
    
    def __str__(self):
        return f"Question for {self.survey}"
    
class Student_Response(models.Model):
    """ 
    response model for feedback surveys
    """
   
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('negative', 'Negative'),
        ('neutral', 'Neutral'),
    )
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    text = models.TextField(max_length=1000)
    student = models.ForeignKey(User, limit_choices_to={'user_type':'student'}, on_delete=models.CASCADE)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    
    def __str__(self):
        return f"Response to {self.question} by {self.student}"
    
class Analysis(models.Model):
    """
    analysis model for storing analysis of feedback surveys
    """
    
    survey = models.OneToOneField(Feedback_Survey, on_delete=models.CASCADE)
    good_count = models.IntegerField(default=0)
    neutral_count = models.IntegerField(default=0)
    bad_count = models.IntegerField(default=0)
    top_keywords = models.JSONField(default=list)
    
    def __str__(self):
        return f"Analysis of {self.survey}"