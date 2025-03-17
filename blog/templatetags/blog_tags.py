from django import template
from blog.models import Post, Category
from datetime import datetime, time, timedelta
from django.utils import timezone
register = template.Library()



@register.simple_tag(name='totalposts')
def total_posts():
    posts = Post.objects.filter(status=1).count()
    return posts

@register.simple_tag (name = 'posts')
def function():
    posts = Post.objects.filter(status=1)
    return  posts

@register.filter(name='snippet')
def snippet(value, arg):
    return value[:arg]  + '...'

@register.filter(name='to_datetime')
def to_datetime(date):
    if date:
        # تبدیل date به datetime با زمان 00:00:00
        dt = datetime.combine(date, time(0, 0, 0))
        return timezone.make_aware(dt)
    return None

@register.inclusion_tag('blog/blog-popular-post.html')
def latestpost(arg=3):
    posts = Post.objects.filter(status=1).order_by('-published_date')[:arg]
    return {'posts': posts}

@register.inclusion_tag('blog/blog-post-categories.html')
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count()
    return {'categories': cat_dict}

@register.filter(name='persian_date')
def persian_date(value):
    if not value:
        return ''
    
    # تبدیل تاریخ به datetime اگر نیاز باشد
    if hasattr(value, 'date') and callable(value.date):
        # اگر value یک datetime باشد
        date_value = value.date()
    else:
        # اگر value یک date باشد
        date_value = value
    
    # بررسی اگر تاریخ امروز است
    today = datetime.now().date()
    if date_value == today:
        return 'امروز'
    
    # بررسی اگر تاریخ دیروز است
    yesterday = (datetime.now() - timedelta(days=1)).date()
    if date_value == yesterday:
        return 'دیروز'
    
    # برای تاریخ‌های قدیمی‌تر، تاریخ را به فارسی نمایش می‌دهیم
    # این فقط یک مثال ساده است، می‌توانید از کتابخانه‌های تبدیل تاریخ شمسی استفاده کنید
    month_names = {
        1: 'فروردین',
        2: 'اردیبهشت',
        3: 'خرداد',
        4: 'تیر',
        5: 'مرداد',
        6: 'شهریور',
        7: 'مهر',
        8: 'آبان',
        9: 'آذر',
        10: 'دی',
        11: 'بهمن',
        12: 'اسفند'
    }
    
    return f"{date_value.day} {month_names.get(date_value.month, '')} {date_value.year}"

