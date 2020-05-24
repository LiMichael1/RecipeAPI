from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                         PermissionsMixin


# build off of default base user manager class
class UserManager(BaseUserManager):
    # override create_user in BaseUserManager
    def create_user(self, email, password=None, **extra_fields):
        """Creates and Saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        # Create new model and normalizes the email
        # to support upper and lower case of same email address
        user = self.model(email=self.normalize_email(email), **extra_fields)
        # Encrypts and sets the password
        user.set_password(password)
        # save the User model
        user.save(using=self._db)  # 'using' for supporting multiple databases

        return user

    # Admins
    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# build off AbstractBaseUser + PermissionMixin
class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""

    # Defining the user model fields
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    # change username field to equal email
    USERNAME_FIELD = 'email'
