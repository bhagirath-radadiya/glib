from django.db import models
from model_utils import Choices
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel
from django.utils import timezone
from complaintApp.managers import CustomUserManager

# Create your models here.


class UserMaster(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    ROLE = Choices(
        ('user', _('User')),
        ('worker', _('worker'))
    )

    email = models.EmailField(unique=True)
    custom_password = models.CharField(max_length=10)
    role = models.CharField(max_length=256, choices=ROLE, default=ROLE.user)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def save(self, *args, **kwargs):
        if not self.is_superuser:
            self.set_password(self.custom_password)
        super(UserMaster, self).save(*args, **kwargs)


class ComplaintMaster(TimeStampedModel):
    STATUS = Choices(
        ('pending', _('Pending')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed'))
    )
    complaint = models.TextField()
    status = models.CharField(max_length=256, choices=STATUS, default=STATUS.pending)
    created_by = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="complaint_master_created_by")
    updated_by = models.ForeignKey(UserMaster, on_delete=models.CASCADE, related_name="complaint_master_updated_by", null=True, blank=True)

    def __str__(self):
        return self.complaint
