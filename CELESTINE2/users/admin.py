from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([CustomUser,Units,Clubs,Students,Python,Javascript,Java,Sql,Php,pythonAttendance,jsAttendance,sqlAttendance,phpAttendance])

