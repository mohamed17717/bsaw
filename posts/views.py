from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse

from django.urls import reverse

from .models import Post, Category
from marketing.models import Signup


def get_category_count():
    qs = Post\
        .objects\
        .values('categories__title')\
        .annotate(Count('categories__title'))
    return qs


def search(request):
    query = request.GET.get('q')

    qs = []
    if query:
        qs = Post.objects.all()
        qs = qs.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query),
        ).distinct()

    context = {'posts': qs[:40]}

    return render(request, 'search_result.html', context)


def category_filter(request, title):
    qs = Post.objects.all()
    qs = qs.filter(categories__title=title)

    context = {'posts': qs[:40]}
    return render(request, 'search_result.html', context)


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        if not email:
            return HttpResponseBadRequest()

        elm = Signup(email=email)
        elm.save()

    featured_posts = Post.objects.filter(featured=True)[:10]
    latest_posts = Post.objects.all().order_by('-timestamp')[:6]
    context = {
        'featured_posts': featured_posts,
        'latest_posts': latest_posts
    }
    return render(request, 'index.html', context)


def blog(request):
    requestedPageVar = 'page'
    page = int(request.GET.get(requestedPageVar, 1))

    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    try:
        paginated_qs = paginator.page(page)
    except PageNotAnInteger:
        paginated_qs = paginator.page(1)
    except EmptyPage:
        paginated_qs = paginator.page(paginator.num_pages)

    context = {
        'posts': paginated_qs,
        'requested_page_var': requestedPageVar,
        'categories': get_category_count(),
        'latest_posts': posts[:6]
    }

    return render(request, 'blog.html', context)


def post(request, id):
    posts = Post.objects.all().order_by('-timestamp')

    post = get_object_or_404(Post, id=id)

    post.seen_count += 1
    post.save()

    next_post = posts.filter(id=id+1).first()
    previous_post = posts.filter(id=id-1).first()

    context = {
        'post': post,
        'categories': get_category_count(),
        'latest_posts': posts[:6],
        'next_post': next_post,
        'previous_post': previous_post,
    }
    return render(request, 'post.html', context)
