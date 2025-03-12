from django.shortcuts import render
from website.models import Contact
from website.forms import ContactForm


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def test_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'test.html', {'form': form})
    form = ContactForm()
    return render(request, 'test.html', {'form': form})

def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

