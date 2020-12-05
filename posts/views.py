from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from django.urls import reverse

from .models import Post, Category, Tag

from datetime import datetime, timedelta

import json
from decorators import require_http_methods, require_fields, allow_fields, check_unique_fields

from pprint import pprint


@require_http_methods(['GET'])
def index(request):
    featured_posts = Post.objects.filter(featured=True)[:10]

    context = {
        'nav_categories': Category.get_nav_categories(5),
        'featured_posts': Post.get_most_viewed_posts_in_last_days(7)[:6],
        'popular_tags': Tag.get_popular_tags(),
        'latest_posts': Post.get_latest_posts(8),
        'most_viewed_posts': Post.get_most_viewed_posts_in_last_days(1)[:20],
        'sidebar_categories': Category.get_sidebar_categories(),
        'footer_categories': Category.get_top_categories(10)
    }

    return render(request, 'home.html', context)


def post(request, id):
    post = get_object_or_404(Post, id=id)

    post.seen_count += 1
    post.save()

    next_post = Post.objects.filter(id=id+1).first()
    previous_post = Post.objects.filter(id=id-1).first()

    context = {
        'nav_categories': Category.get_nav_categories(5),
        'most_viewed_posts': Post.get_most_viewed_posts_in_last_days(1)[:20],
        'sidebar_categories': Category.get_sidebar_categories(),
        'footer_categories': Category.get_top_categories(10),

        'post': post,
        'next_post': next_post,
        'previous_post': previous_post,
    }

    return render(request, 'post.html', context)


def paginatePosts(qs, page):
    paginator = Paginator(qs, 12)
    try:posts = paginator.page(page)
    except:posts = []
    return posts

def listPosts(view_name):
    views = {
        'latest_posts': {
            'qs': lambda *args, **kwargs: Post.objects.all().order_by('-created'),
            'dir_name': lambda *args, **kwargs: 'اّخر الأخبار',
            'dir_url': lambda *args, **kwargs: '/latest/posts/',
        },

        'tag_posts': {
            'qs': lambda title,  *args, **kwargs: Post.objects.filter(tags__title=title).order_by('-created'),
            'dir_name': lambda title, *args, **kwargs: title,
            'dir_url': lambda title, *args, **kwargs: reverse('tag-filter', kwargs={'title':title}),
        },

        'category_posts': {
            'qs': lambda title,  *args, **kwargs: Post.objects.filter(categories__title=title).order_by('-created'),
            'dir_name': lambda title, *args, **kwargs: title,
            'dir_url': lambda title, *args, **kwargs: reverse('category-filter', kwargs={'title':title}),
        },

        'search_posts': {
            'qs': lambda query,  *args, **kwargs: Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__title__icontains=query) | Q(categories__title__icontains=query),).distinct(),
            'dir_name': lambda query, *args, **kwargs: query,
            'dir_url': lambda query, *args, **kwargs: reverse('search', kwargs={'query':query}),
        },
    }

    def view(request, *args, **kwargs):
        page = request.GET.get('page', 1)
        try: page = int(page)
        except: page = 1

        view_obj = views.get(view_name)

        posts_qs = view_obj['qs'](*args, **kwargs)

        context = {
            'posts': paginatePosts(posts_qs, page),
            'dir_name': view_obj['dir_name'](*args, **kwargs),
            'dir_url': view_obj['dir_url'](*args, **kwargs),
            'posts_length': len(posts_qs),

            'next_page': page + 1,

            'nav_categories': Category.get_nav_categories(5),
            'most_viewed_posts': Post.get_most_viewed_posts_in_last_days(1)[:20],
            'sidebar_categories': Category.get_sidebar_categories(),
            'footer_categories': Category.get_top_categories(10)
        }

        return render(request, 'list.html', context)
    return view


# static views
def static_template(templateName):
    def view(request):
        return render(request, templateName, {})
    return view


@require_http_methods(['POST'])
@require_fields(['url', 'title', 'thumbnailURL', 'content'])
@allow_fields(['url', 'title', 'thumbnailURL', 'content', 'categories', 'tags', 'date', 'small_summery', 'overview'])
@check_unique_fields(Post, ['url'])
def create_post(request):
    data = json.loads(request.body.decode('utf-8'))  # .dict()

    print(data)

    categories = data.pop('categories', [])
    tags = data.pop('tags', [])

    categoriesObjects = [Category.get_category_by_name(
        category, forced=True) for category in categories]
    tagsObjects = [Tag.get_tag_by_name(
        tag, forced=True) for tag in tags]

    post = Post.objects.create(**data)
    print('\n\n POST: ', post.title, '\n\n')

    post.set_categories(categoriesObjects)
    post.set_tags(tagsObjects)

    return HttpResponse(status=200)
