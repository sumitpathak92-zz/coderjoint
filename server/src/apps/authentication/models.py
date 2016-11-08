from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        username = ''
        if not email:
            raise ValueError("Please enter valid email id")
        if not kwargs.get('username'):
            username = 'sumitpathak92'
            print "Please enter valid username"
        else:
            username = kwargs.get('username')

        account = self.model(
                email=self.normalize_email(email), username=username
                )
        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, password, **kwargs):
        print "create superuser called here"
        account = self.create_user(email, password, **kwargs)
        account.is_admin = True
        account.save()
        return account


class UserAccount(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20,blank=True)
    about_me = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=50, blank=True)
    exp_type = models.CharField(max_length=10, blank=True)

    joined_on = models.DateTimeField(auto_now_add=True)
    profile_last_updated = models.DateTimeField(auto_now=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username']

    #overwriting unicode method to change the default behavior
    def __unicode__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_username(self):
        return self.username

    class Meta:
        db_table = 'coderjoint_users_basic_info'
