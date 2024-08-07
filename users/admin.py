from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(User)

admin.site.register(Universities)

admin.site.register(Department)

admin.site.register(Course)

admin.site.register(Feedback_Survey)

admin.site.register(Question)

admin.site.register(Student_Response)

admin.site.register(Analysis)
