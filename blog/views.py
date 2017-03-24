from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.shortcuts import render, redirect

from blog.models import Article

# Create your views here.

def home(request):
    posts = Article.objects.all()
    paginator = Paginator(posts, 3)
    page = request.GET.get('page')
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.paginator(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list})

def detail(request, id):
    try:
        post = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'post.html', {'post': post})

def archives(request):
    try:
        post_list = Article.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'archives.html', {'post_list': post_list,
                                             'error': False})
def search_tag(request, tag):
    try:
        post_list = Article.objects.filter(category__iexact=tag)
        # A case-insensitive match. So, the query:
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'tag.html', {'post_list': post_list})

def blog_search(request):
    if 'search' in request.GET:
        search = request.GET['search']
        if not search:
            return render(request, 'home.html')
        else:
            post_list = Article.objects.filter(title__icontains=search)
            #case-insensitive containment test
            if not len(post_list):
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': True})
            else:
                return render(request, 'archives.html', {'post_list': post_list,
                                                         'error': False})
    return redirect('/')



