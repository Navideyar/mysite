from django.shortcuts import render, get_object_or_404
from blog.models import Post, Category , Comment 
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from .forms import CommentForm

# Create your views here.
def blog_view(request, cat_name=None, author_username=None, tag_name=None):
    posts = Post.objects.filter(status=1)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)
    if tag_name:
        posts = posts.filter(tags__name=tag_name)
    
    posts = Paginator(posts, 2)
    try:
        page_number = request.GET.get("page")
        posts = posts.get_page(page_number)
    except:
        posts = posts.get_page(1)
    

    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)


def blog_single(request, pid):
    post = get_object_or_404(Post, pk=pid)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post  # اینجا post را به comment اضافه می‌کنیم
            comment.save()
            messages.add_message(request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد")
        else:
            messages.add_message(request, messages.ERROR, "نظر شما ثبت نشد")
            
    posts = Post.objects.filter(status=1)
    
    # افزایش تعداد بازدید
    post.counted_views += 1
    post.save()
    
    # دریافت کامنت‌های مربوط به این پست از دیتابیس
    comments = Comment.objects.filter(post=post.id, approved=True)
    form = CommentForm()
    context = {"post": post, "comments": comments, "form": form}
    
    return render(request, "blog/blog-single.html", context)


def test(request):
    return render(request, "test.html")


def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)
   
def blog_search(request):
    posts = Post.objects.filter(status=1)
    if request.method == "GET":
        if s := request.GET.get("s"):
            posts = posts.filter(Q(content__icontains=s) | Q(title__icontains=s))
        
    context = {"posts": posts}
    return render(request, "blog/blog-home.html", context)

