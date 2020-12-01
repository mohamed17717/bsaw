from django.db import models
from django.db.models import Subquery, Count, Sum
from django.contrib.auth import get_user_model
from django.urls import reverse

from tinymce import HTMLField

from datetime import datetime, timedelta
import random

User = get_user_model()


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.id, filename)


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)
    css_icon_class = models.CharField(max_length=64, blank=True, null=True)
    css_icon_color = models.CharField(max_length=32, blank=True, null=True)
# flaticon-runer-silhouette-running-fast
    is_nav = models.BooleanField(default=False)
    is_home_sidebar = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-filter', kwargs={'title': self.title})

    def get_posts(self):
        return self.post_category.all()

    @staticmethod
    def get_nav_categories(count=5):
        return Category.objects.filter(is_nav=True)[:count]

    @staticmethod
    def get_sidebar_categories(count=3):
        return Category.objects.filter(is_home_sidebar=True)[:count]

    @staticmethod
    def get_category_by_name(name, forced=False):
        category = Category.objects.filter(title=name).first()
        if not category and forced:
            category = Category.objects.create(title=name)

        return category

    @staticmethod
    def get_top_categories(count):
        return Category\
            .objects.all()\
            .annotate(count=Sum('post_category__seen_count'))\
            .order_by('-count')[:count]


class Tag(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag-filter', kwargs={'title': self.title})

    def get_posts(self):
        return self.post_tag.all()

    @staticmethod
    def get_popular_tags():
        # posts in last 3 days
        # order on most seen
        # last 100 post
        # list tags and order on its repetation
        qs = Post.get_most_viewed_posts_in_last_days(3)\
            .values('tags__title')\
            .annotate(count=Count('tags__title'))\
            .order_by('-count')[:10]
        return qs

    @staticmethod
    def get_tag_by_name(name, forced=False):
        tag = Tag.objects.filter(title=name).first()
        if not tag and forced:
            tag = Tag.objects.create(title=name)

        return tag


class Post(models.Model):
    # data must be from any blog
    url = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    thumbnailURL = models.URLField(max_length=200)
    content = HTMLField('Content')

    # relational fields
    categories = models.ManyToManyField(Category, related_name='post_category')
    tags = models.ManyToManyField(Tag, related_name='post_tag')

    # extras || calculated
    date = models.CharField(max_length=256, blank=True, null=True)
    small_summery = models.CharField(max_length=256, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)

    # use cron job to convert url into an image
    thumbnail = models.ImageField(blank=True, null=True)

    # default fields
    created = models.DateTimeField(auto_now_add=True)
    seen_count = models.IntegerField(default=0)
    fake_seen_count = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)

    # not used now
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk: # created
            if not self.seen_count:
                fake_seens = random.randint(100, 500)
                self.seen_count = fake_seens
                self.fake_seen_count = fake_seens

        return super(Post, self).save(*args, **kwargs) 

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.id})

    def set_categories(self, categories):
        self.categories.set(categories)

    def set_tags(self, tags):
        self.tags.set(tags)

    @staticmethod
    def get_latest_posts(count=20):
        return Post.objects.all().order_by('-created')[:count]

    @staticmethod
    def get_posts_in_last_days(days=3):
        since = datetime.now() - timedelta(days=days)
        qs = Post.objects.filter(created__gt=since)
        return qs

    @staticmethod
    def get_most_viewed_posts_in_last_days(days=3):
        qs = Post.get_posts_in_last_days(days).order_by('-seen_count')
        return qs
