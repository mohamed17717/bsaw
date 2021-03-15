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

def get_defualt_context(request=None):
    return {
        # 'most_viewed_posts': Post.get_most_viewed_posts_in_last_days(2, 20),
        'popular_posts': Post.get_most_viewed_posts_in_last_days(1000, 5),
        'latest_posts': Post.get_latest_posts(5),
        'random_post': Post.get_random_post(),
        'random_posts': [Post.get_random_post() for _ in range(15)],

        'current_url': request.build_absolute_uri() if request else '', # {% abs_url 'post-detail' post.pk %}
        'site_name': 'سواح ميديا',
        # 'current_tab': 'news'
    }


@require_http_methods(['GET'])
def index(request):
    context = { 
        **get_defualt_context(), 
        'home_latest_posts': Post.objects.all().order_by('-pk')[:10],
        'site_categories': filter(lambda item: item['count'] > 0, [
                { 'title': cat.title, 'count': cat.get_posts().count(), 'url': cat.get_absolute_url } 
                for cat in Category.objects.all()
        ])
    }

    categories = [
        (6, 'cat_news', 'الاخبار'),
        (5, 'cat_sport', 'الرياضة'),
        (3, 'cat_lifestyle', 'لايف ستايل'),
        (3, 'cat_health', 'الصحة والجمال'),
        (9, 'cat_mix', 'منوعات'),
        (4, 'cat_article', 'مقالات'),
    ]

    for count, context_name, category_name in categories:
        category = Category.get_category_by_name(category_name)
        if not category: continue

        context[context_name] = {
            'url': category.get_absolute_url(),
            'title': category.title,
            'posts': category.get_posts().order_by('-pk')[:count]
        }

    
    return render(request, 'home.html', context)


def post(request, pk):
    # post = get_object_or_404(Post, pk=pk)

    context = {
        **get_defualt_context(),
        'post': Post.get_by_pk(pk),
        # 'next_post': Post.objects.filter(id=id+1).first(),
        # 'previous_post': Post.objects.filter(id=id-1).first(),
    }

    print('\n\n')
    pprint(context)
    print('\n\n')

    return render(request, 'post.html', context)


def paginatePosts(qs, page):
    paginator = Paginator(qs, 12)

    try:
        posts = paginator.page(page)
    except:
        posts = []

    return {'list': posts, 'pg': paginator}

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
            'dir_name': lambda query, *args, **kwargs: f'البحث عن: {query}',
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
            **get_defualt_context(),

            'posts': paginatePosts(posts_qs, page),
            'list_title': view_obj['dir_name'](*args, **kwargs),
            'dir_url': view_obj['dir_url'](*args, **kwargs),
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
@allow_fields(['url', 'title', 'thumbnailURL', 'content', 'categories', 'tags', 'date', 'small_summery', 'overview', 'creator'])
@check_unique_fields(Post, ['url'])
def create_post(request):
    data = json.loads(request.body.decode('utf-8'))  # .dict()
    # print(data)
    categories = data.pop('categories', [])
    tags = data.pop('tags', [])

    categoriesObjects = [Category.get_category_by_name(
        category, forced=True) for category in categories]
    tagsObjects = [Tag.get_tag_by_name(
        tag, forced=True) for tag in tags]

    post = Post.objects.create(**data)
    # print('\n\n POST: ', post.title, '\n\n')

    post.set_categories(categoriesObjects)
    post.set_tags(tagsObjects)

    return HttpResponse(status=200)
