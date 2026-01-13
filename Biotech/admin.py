from django.contrib import admin
from .models import Enquiry,Login,session,Course,tbl_student
# Register your models here.
admin.site.register(Enquiry)
admin.site.register(Login)
admin.site.register(session)
admin.site.register(Course)
admin.site.register(tbl_student)