from django.contrib import admin
from complaintApp.models import UserMaster, ComplaintMaster

# Register your models here.

class UserMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'custom_password', 'role']
    search_fields = ['id', 'email', 'custom_password', 'role']

class ComplaintMasterAdmin(admin.ModelAdmin):
    ls = [f.name for f in ComplaintMaster._meta.get_fields()]
    list_display = ls
    search_fields = ls


admin.site.register(UserMaster, UserMasterAdmin)
admin.site.register(ComplaintMaster, ComplaintMasterAdmin)