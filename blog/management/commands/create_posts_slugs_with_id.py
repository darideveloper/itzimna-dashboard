import os

from django.core.management.base import BaseCommand

from blog import models

BASE_FILE = os.path.basename(__file__)


class Command(BaseCommand):
    help = "Set all current post as slug value to: id-current-slug"

    def handle(self, *args, **kwargs):
        posts = models.Post.objects.all()

        for post in posts:
            print(f"Saving post {post.id} - {post.title}")
            post.slug = f"{post.id}-{post.slug}"
            post.save()
