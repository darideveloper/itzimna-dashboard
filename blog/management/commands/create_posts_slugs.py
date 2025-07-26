import os

from django.core.management.base import BaseCommand

from blog import models

BASE_FILE = os.path.basename(__file__)


class Command(BaseCommand):
    help = "Save all posts to get their slugs"

    def handle(self, *args, **kwargs):
        posts = models.Post.objects.all()

        for post in posts:
            print(f"Saving post {post.id} - {post.title}")
            post.save()
