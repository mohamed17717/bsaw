from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse

from django.urls import reverse

from .models import Post, Category, Tag, Twt

from datetime import datetime, timedelta

import json
from decorators import require_http_methods, require_fields, allow_fields, check_unique_fields, cache_request

from pprint import pprint

def get_today_date():
    days_map = [
        ('Monday', 'الأثنين'),
        ('Tuesday', 'الثلاثاء'),
        ('Wednesday', 'الاربعاء'),
        ('Thursday', 'الخميس'),
        ('Friday', 'الجمعة'),
        ('Saturday', 'السبت'),
        ('Sunday', 'الاحد'),
    ]

    months_map = [
        ('01', 'يناير'),
        ('02', 'فبراير'),
        ('03', 'مارس'),
        ('04', 'ابريل'),
        ('05', 'مايو'),
        ('06', 'يونيو'),
        ('07', 'يوليو'),
        ('08', 'اغسطس'),
        ('09', 'سبتمبر'),
        ('10', 'اكتوبر'),
        ('11', 'نوفمبر'),
        ('12', 'ديسمبر'),
    ]

    date = datetime.today().strftime("%A, %m   %d %Y")
    day_month_ar = datetime.today().strftime("%A, %m")

    maps = days_map+months_map
    for en, ar in maps:
        if en in day_month_ar:
            day_month_ar = day_month_ar.replace(en, ar)

    return date.replace(datetime.today().strftime("%A, %m"), day_month_ar)


@cache_request('default_context', timeout=60*60*12)
def get_defualt_context(request=None):
    return {
        # 'most_viewed_posts': Post.get_most_viewed_posts_in_last_days(2, 20),
        'popular_posts': Post.get_most_viewed_posts_in_last_days(1000, 5),
        'latest_posts': Post.get_latest_posts(5),
        'random_post': Post.get_random_post(),
        'random_posts': [Post.get_random_post() for _ in range(15)],

        'current_url': request.build_absolute_uri() if request else '',
        'site_name': 'مكساوي',

        'today_date': get_today_date(),
        'current_tab_class': 'current-menu-item current_page_item tie-current-menu',

        'social': {
            'facebook': '',
            'twitter': '',
            'pinterest': '',
            'youtube': '',
            'instagram': '',
            'paypal': '',
        }
    }


@require_http_methods(['GET'])
@cache_request('home_page')
def index(request):
    context = { 
        **get_defualt_context(), 
        'current_tab': 'الرئيسية',

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


@cache_request('post_{pk}', timeout=60*60*3, identifier='pk')
def post(request, pk):
    post = Post.get_by_pk(pk)
    context = {
        **get_defualt_context(),
        'current_tab': post.category.title if post.category else '',
        'post': post,
    }

    return render(request, 'post.html', context)


def paginatePosts(qs, page):
    paginator = Paginator(qs, 12)

    try:
        posts = paginator.page(page)
    except:
        posts = []

    return {'list': posts, 'pg': paginator}

def listPosts(view_name):
    context = {'current_tab': 'xx'}
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
            'qs': lambda title,  *args, **kwargs: Category.get_category_by_name(title).get_posts().order_by('-created'),
            'dir_name': lambda title, *args, **kwargs: title,
            'dir_url': lambda title, *args, **kwargs: reverse('category-filter', kwargs={'title':title}),
        },

        'search_posts': {
            'qs': lambda query,  *args, **kwargs: Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__title__icontains=query) | Q(category__title__icontains=query) | Q(sub_category__title__icontains=query),).distinct().order_by('-created'),
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
            'current_tab': view_obj['dir_name'](*args, **kwargs),
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
@require_fields(['url', 'title', 'thumbnailURL', 'content', 'category'])
@allow_fields(['url', 'title', 'thumbnailURL', 'thumbnailURL_large', 'content', 'category', 'sub_category', 'tags', 'date', 'small_summery', 'overview', 'description', 'source', 'creator',])
@check_unique_fields(Post, ['url'])
def create_post(request):
    data = json.loads(request.body.decode('utf-8'))  # .dict()

    category = data.pop('category', None)
    sub_category = data.pop('sub_category', None)
    tags = data.pop('tags', [])

    tagsObjects = [Tag.get_tag_by_name(tag, forced=True) for tag in tags]

    post = Post.objects.create(**data)

    categoryObject = Category.get_category_by_name(category, forced=True)
    post.category = categoryObject
    if sub_category:
        subCategoryObject = Category.get_category_by_name(sub_category, forced=True)
        post.sub_category = subCategoryObject
    post.save()
    post.set_tags(tagsObjects)

    return HttpResponse(status=200)

@require_http_methods(['POST'])
@require_fields(['key', 'account'])
def add_twt(request):
    data = request.POST.dict()

    account = data['account']
    key = data['key']

    if key != 'eft7 ya 3m ana omda':
        return HttpResponseBadRequest('not valid key')

    Twt.objects.create(account=account)

    return HttpResponse(status=201)

