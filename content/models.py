from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=300)
    link = models.URLField(max_length=200, validators=[URLValidator])
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)
    up_votes = models.BigIntegerField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_posts"
    )
    users_voted = models.ManyToManyField(User)

    def __str__(self):
        return self.link

    def get_author(self):
        return self.author

    def get_comments(self):
        return list(self.post_comments.all())

    def get_users_voted(self):
        return list(self.users_voted.all())

    def when_published(self):
        now = timezone.now()
        since = now - self.creation_date
        days = since.days
        seconds = since.seconds

        if days == 0:
            if seconds >= 3600:
                return f"{int(seconds/3600)} hours ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        else:
            return f"{days} days ago"


class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="post_comments"
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="author_comments"
    )
    up_votes = models.BigIntegerField()
    users_voted = models.ManyToManyField(User)
    creation_date = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.content

    def get_author(self):
        return self.author

    def get_post(self):
        return self.post

    def get_users_voted(self):
        return list(self.users_voted.all())

    def when_published(self):
        now = timezone.now()
        since = now - self.creation_date
        days = since.days
        seconds = since.seconds

        if days == 0:
            if seconds >= 3600:
                return f"{int(seconds/3600)} hours ago"
            else:
                return f"{int(seconds / 60)} minutes ago"
        else:
            return f"{days} days ago"
