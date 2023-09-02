from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,AbstractUser

# custom manager
class UserManager(BaseUserManager):
    def create_user(self,username,email,password=None,**extra_fields):
        if not email:
            raise ValueError('User mush have an Email Address')
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username,email,password=None):
        user = self.create_user(
            username,
            email,
            password=password,
        )
        user.is_admin=True
        user.save(using=self._db)
        return user
    
    
# custom user
class User(AbstractBaseUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True,
                              max_length=255,
                              verbose_name='Email')
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to='profile_photo/')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = UserManager()
    
    def __str__(self):
        return self.username
    
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def has_perm(self,perm,obj=None):
        "Does this user have a specific permission?"
        return self.is_admin
    
    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin
