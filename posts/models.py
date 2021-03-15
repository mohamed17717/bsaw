from django.db import models
from django.db.models import Subquery, Count, Sum, F, Max
from django.contrib.auth import get_user_model
from django.urls import reverse

from django.shortcuts import get_object_or_404

from tinymce import HTMLField

from datetime import datetime, timedelta
import random

import jsonfield

User = get_user_model()


def post_default_seen_count():
    return random.randint(100, 500)


def get_random_obj(myModel=None, qs=None):
    assert qs != None or myModel != None

    if not qs:
        qs = myModel.objects.all()

    max_id = qs.aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        obj = qs.filter(pk=pk).first()
        if obj:
            return obj

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)
    main_category = models.ForeignKey("self", related_name='sub_categories', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category-filter', kwargs={'title': self.title})

    def get_posts(self):
        return self.category_posts.all()

    def get_static_blog_category_path(self):
        category_path = ['الرئيسية']
        if self.main_category: category_path.append(self.main_category)
        category_path.append(self.title)

        return '/'.join(category_path)

    @staticmethod
    def get_category_by_name(name, forced=False):
        category = Category.objects.filter(title=name).first()
        if not category and forced:
            category = Category.objects.create(title=name)

        return category

    @staticmethod
    def get_top_categories(count):
        return Category\
            .objects.all()
            # .annotate(count=Sum('post_category__seen_count'))\
            # .order_by('-count')[:count]


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
        qs = Post.get_most_viewed_posts_in_last_days(3, 20)\
            # .values('tags__title')
            # \
            # .annotate(count=Count('tags__title'))\
            # .order_by('-count')[:10]

        tags_tacker = {}
        for item in qs:
            # print(item.tags.all())
            for tag in item.tags.all():
                tag_title = tag.title
                if tags_tacker.get(tag_title):
                    tags_tacker[tag_title] += 1
                else:
                    tags_tacker[tag_title] = 1

        tags = [{'tags__title': tag_name, 'count': count} for tag_name, count in tags_tacker.items()]
        tags.sort(key=lambda i: i['count'])

        return tags[:20]

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
    thumbnailURL_large = models.URLField(max_length=200, blank=True, null=True)
    content = HTMLField('Content')

    # relational fields
    # categories = models.ManyToManyField(Category, related_name='post_category')
    category = models.ForeignKey(Category, related_name='category_posts', on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey(Category, related_name='sub_category_posts', on_delete=models.SET_NULL, blank=True, null=True)
    tags = models.ManyToManyField(Tag, related_name='tag_posts')

    related_posts = jsonfield.JSONField(blank=True, null=True) # array of posts

    # extras || calculated
    date = models.CharField(max_length=256, blank=True, null=True)
    small_summery = models.CharField(max_length=256, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=256, blank=True, null=True)

    # use cron job to convert url into an image
    thumbnail = models.ImageField(blank=True, null=True)

    # default fields
    created = models.DateTimeField(auto_now_add=True)
    seen_count = models.IntegerField(default=post_default_seen_count)
    featured = models.BooleanField(default=False)

    # not used now
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    creator = models.CharField(max_length=16, default='admin') # admin or bot

    def __str__(self):
        return f'{self.id} | {self.title}'

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def set_categories(self, categories):
        self.categories.set(categories)

    def set_tags(self, tags):
        self.tags.set(tags)

    def serialize_as_related_post(self):
        return {
            'thumbnailURL': self.thumbnailURL,
            'title': self.title,
            'url': self.get_absolute_url(),
            'date': self.date
        }
    
    def serialize_as_fast_news(self):
        return {
            'title': self.title,
            'url': self.get_absolute_url(),
        }

    def get_static_blog_category_path(self):
        category_path = ['الرئيسية']
        if self.category: category_path.append(self.category)
        if self.sub_category: category_path.append(self.sub_category)
        category_path.append(self.title)

        return '/'.join(category_path)

    def get_category(self):
        return self.sub_category or self.category

    @staticmethod
    def get_latest_posts(count=20):
        return Post.objects.all().order_by('-created')[:count]

    @staticmethod
    def get_posts_in_last_days(days=3):
        since = datetime.now() - timedelta(days=days)
        qs = Post.objects.filter(created__gt=since)
        return qs

    @staticmethod
    def get_most_viewed_posts_in_last_days(days=3, count=10):
        # qs = Post.get_posts_in_last_days(days).annotate(visits=F('seen_count') - F('fake_seen_count')).order_by('-visits')
        qs = Post.get_posts_in_last_days(days).order_by('-seen_count')
        if count:
            qs = qs[:count]
        return qs

    @staticmethod
    def get_featured_posts(count, force_count=False):
        qs = Post.objects.filter(featured=True)
        got_posts = len(qs)
        if force_count and got_posts < count:
            more_qs = Post.get_most_viewed_posts_in_last_days(3, count-got_posts)

        return [*qs, *more_qs]

    @staticmethod
    def get_by_pk(pk):
        post = get_object_or_404(Post, pk=pk)

        if not post.related_posts:
            category = post.category or post.sub_category
            if category:
                related_posts = category.category_posts.all()
            else:
                related_posts = Post.objects.all()

            random_related_posts = [
                get_random_obj(qs=related_posts).serialize_as_related_post()
                for _ in range(2)
            ]

            post.related_posts = random_related_posts

        post.seen_count += 1

        post.save()

        return post

    @staticmethod
    def get_random_post():
        return get_random_obj(myModel=Post)
