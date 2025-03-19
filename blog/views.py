from django.shortcuts import render, get_object_or_404 , redirect
from blog.models import Post, Category , Comment 
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage , PageNotAnInteger
from django.contrib import messages
from .forms import CommentForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def blog_view(request, cat_name=None, author_username=None, tag_name=None):
    posts = Post.objects.filter(status=1)
    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)
    if tag_name:
        posts = posts.filter(tags__name=tag_name)
    
    posts = Paginator(posts, 4)
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
            comment.post = post
            comment.save()
            messages.add_message(request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد")
        else:
            messages.add_message(request, messages.ERROR, "نظر شما ثبت نشد")
            
    posts = Post.objects.filter(status=1)
    
    # افزایش تعداد بازدید
    post.counted_views += 1
    post.save()
    
    if not post.login_required:
        comments = Comment.objects.filter(post=post.id, approved=True)
        form = CommentForm()
        context = {"post": post, "comments": comments, "form": form}
        return render(request, "blog/blog-single.html", context)
    else:
        if not request.user.is_authenticated:
            next_url = request.path
            login_url = reverse('accounts:login')
            return redirect(f"{login_url}?next={next_url}")
        else:
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

