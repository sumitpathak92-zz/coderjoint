from django.db import models

from apps.authentication.models import UserAccount


class Post(models.Model):
    author = models.ForeignKey(UserAccount)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0}'.format(self.content)

    class Meta:
        db_table = 'coderjoint_users_posts'
