from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from website.models import Contact, Newsletter
from website.forms import NameForm, ContactForm, NewsletterForm


def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,"about.html")

def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'پیام شما با موفقیت ارسال شد.')
            return redirect('website:contact')
        else:
            messages.add_message(request, messages.ERROR, 'لطفاً تمام فیلدها را پر کنید.')
    form = ContactForm()
    return render(request, "contact.html", {'form': form})


def newsletter_view(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('website:home'))
        else:
            return HttpResponseRedirect(reverse('website:home'))
    return HttpResponseRedirect(reverse('website:home'))
  

