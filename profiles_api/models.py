from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
#need the above two classes when overriding or customizing the default Django user model
from django.contrib.auth.models import BaseUserManager
#need the above to define UserProfileManager function


class UserProfileManager(BaseUserManager):
    """Manager for User Profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email) #second half of email id is case insensitive
        user = self.model(email=email, name=name)

        user.set_password(password) #hash the password to protect it
        user.save(using=self._db) #save user in database

        return user

    def create_superuser(self, email, name, password):
        """Create new super user with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True #function automatically created by PermissionsMixin
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default = False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email
