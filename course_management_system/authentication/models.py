from django.db import models
from django.contrib.auth.models import AbstractUser ,  UserManager
from datetime import datetime

# Create your models here.


class NonDeleted(models.Manager):
    def active(self):
        return self.get_queryset().filter(deleted_at__isnull=True)
    
class UserNonDeleted(UserManager):
    def active(self):
        return self.get_queryset().filter(deleted_at__isnull=True)    


class Base(models.Model):
    deleted_at = models.DateTimeField(default=None, null=True , blank = True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = NonDeleted()

    def soft_delete(self):
        self.deleted_at = datetime.now()
        self.save()

    class Meta:
        abstract = True


class User(AbstractUser, Base):
    role = models.CharField(
        max_length=9,
        choices=[("admin", "Admin"), ("student", "Student"), ("teacher", "Teacher")],
    )
    objects = UserNonDeleted()

    REQUIRED_FIELDS = []
