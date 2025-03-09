from idlelib.rpc import request_queue

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, HttpResponseRedirect, Http404
from django.contrib import messages
from .models import Post
from .forms import PostForm, CommentForm
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

def search_posts(request):
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = post_list.filter(Q(title__icontains = query) |
                                     Q(text__icontains = query) |
                                     Q(user__first_name__icontains = query) |
                                     Q(user__last_name__icontains = query)).distinct()
    return render(request, "search_results.html", {"results": post_list, "query": query})

def post_index(request):
    # query = request.GET.get('q')
    # if query:
    #     post_list = post_list.filter(Q(title__icontains = query) |
    #                                  Q(text__icontains = query) |
    #                                  Q(user__first_name__icontains = query) |
    #                                  Q(user__last_name__icontains = query)).distinct()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 5)  # Show 5 contacts per page

    page = request.GET.get('sayfa')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)
    return  render(request, 'post/index.html', {'posts' : posts})

def post_detail(request, slug):
    post = get_object_or_404(Post, slug = slug)
    form = CommentForm(request.POST or None)
        #Formdan gelen bilgileri kaydet
    if form.is_valid():
        comment = form.save(commit = False)
        comment.post = post
        comment.save()
        messages.success(request, 'Başarılı bir şekilde oluşturdunuz.')
        return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'post' : post,
        'form' : form,
    }
    return render(request, 'post/detail.html', context)

def post_create(request):

    if not request.user.is_authenticated:
        return Http404()
    #YÖNTEM 1
    # form_title = request.POST.get('title')    eski usul alınabilecek şekilde
    # form_text = request.POST.get('text')
    # Post.objects.create(title = form_title, text = form_text)
    # form = PostForm(request.POST or None)

    # YÖNTEM 2 ÖNERİLEN GPT
    if request.method == "POST":
        #Formdan gelen bilgileri kaydet
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit = False)
            post.user = request.user
            post.save()
            messages.success(request, 'Başarılı bir şekilde oluşturdunuz.')
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        #Formu kullanıcıya göster
        form = PostForm()

    # YÖNTEM 3 ÖNERİLMEDİ
    # form = PostForm(request.POST or None)
    # if form.is_valid():
    #     form.save()

    context = {
        'form': form,
    }

    return render(request, 'post/form.html', context)

def post_update(request, slug):
    if not request.user.is_authenticated:
        return Http404()
    post = get_object_or_404(Post, slug = slug)
    form = PostForm(request.POST or None, request.FILES or None, instance = post)
    if form.is_valid():
            form.save()
            messages.success(request, 'Başarılı bir şekilde güncellediniz.')
            form = PostForm()
            return HttpResponseRedirect(post.get_absolute_url())
    context = {
        'form': form,
    }
    return render(request, 'post/form.html', context)

def post_delete(request, slug):
    if not request.user.is_authenticated():
        return Http404()
    post = get_object_or_404(Post, slug = slug)
    post.delete()
    return redirect("post:index")

