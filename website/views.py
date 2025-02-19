from django.shortcuts import render

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def test_view(request):
    return render(request, 'test.html', {'name':'navid', 'lastname':'safaie' })