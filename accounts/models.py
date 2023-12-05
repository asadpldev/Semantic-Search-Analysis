from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from .mixins import TimeStampMixin

class CustomUserManger(BaseUserManager):
    def create_user(self, email, full_name=None, username=None, password=None):
        if not email:
            raise ValueError("email is required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username=None, password=None):
        user = self.create_user(email, username=username, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(TimeStampMixin,AbstractBaseUser):
    GENDER = (
        ('male',"Male"),
        ('female',"Female"),
        ('other',"Other"),
        
    )
    email = models.EmailField(max_length=255, unique=True)
    username   = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name  = models.CharField(max_length=255, null=True, blank=True)
    age = models.CharField(max_length=255, default="male")
    gender = models.CharField(max_length=255,default="male",choices=GENDER)
    location = models.CharField(max_length=255, null=True, blank=True)
    profile_pic   = models.ImageField( upload_to ='profile_pics',null = True , blank = True )



    is_active          = models.BooleanField(default=True)
    is_admin           = models.BooleanField(default=False)
    is_staff           = models.BooleanField(default=False)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManger()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return self.is_admin
    
    def get_name(self):
        try:
            return self.first_name[0]+self.last_name[0].capitalize()
        except:
            return self.email
   
    def get_full_name(self):
        try:
            return f"{self.first_name} {self.last_name}"
        except:
            return self.email
