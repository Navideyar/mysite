from django import template
from blog.models import Post, Category
from datetime import datetime, time, timedelta
from django.utils import timezone
register = template.Library()

def convert_to_persian_words(number):
    """تبدیل اعداد به کلمات فارسی"""
    persian_words = {
        0: 'صفر',
        1: 'یک',
        2: 'دو',
        3: 'سه',
        4: 'چهار',
        5: 'پنج',
        6: 'شش',
        7: 'هفت',
        8: 'هشت',
        9: 'نه',
        10: 'ده',
        11: 'یازده',
        12: 'دوازده',
        13: 'سیزده',
        14: 'چهارده',
        15: 'پانزده',
        16: 'شانزده',
        17: 'هفده',
        18: 'هجده',
        19: 'نوزده',
        20: 'بیست',
        30: 'سی',
        40: 'چهل',
        50: 'پنجاه',
        60: 'شصت',
        70: 'هفتاد',
        80: 'هشتاد',
        90: 'نود',
        100: 'صد',
        200: 'دویست',
        300: 'سیصد',
        400: 'چهارصد',
        500: 'پانصد',
        600: 'ششصد',
        700: 'هفتصد',
        800: 'هشتصد',
        900: 'نهصد',
    }
    
    if number in persian_words:
        return persian_words[number]
    
    if number < 100:
        tens = (number // 10) * 10
        ones = number % 10
        if ones == 0:
            return persian_words[tens]
        else:
            return f"{persian_words[tens]} و {persian_words[ones]}"
    
    if number < 1000:
        hundreds = (number // 100) * 100
        remainder = number % 100
        if remainder == 0:
            return persian_words[hundreds]
        else:
            return f"{persian_words[hundreds]} و {convert_to_persian_words(remainder)}"
    
    return str(number)  # برای اعداد بزرگتر از 999

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

@register.filter(name='persian_naturaltime')
def persian_naturaltime(value):
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
    yesterday = (datetime.now() - timezone.timedelta(days=1)).date()
    if date_value == yesterday:
        return 'دیروز'
    
    # برای تاریخ‌های قدیمی‌تر از محاسبه زمان استفاده می‌کنیم
    if timezone.is_naive(value):
        value = timezone.make_aware(value)
    
    now = timezone.now()
    diff = now - value
    
    seconds = diff.total_seconds()
    
    if seconds < 0:
        # اگر زمان انتشار در آینده باشد
        return 'به تازگی'
    elif seconds < 60:
        return 'چند لحظه پیش'
    elif seconds < 3600:  # less than an hour
        minutes = int(seconds // 60)
        return f'{convert_to_persian_words(minutes)} دقیقه پیش'
    elif seconds < 86400:  # less than a day
        hours = int(seconds // 3600)
        return f'{convert_to_persian_words(hours)} ساعت پیش'
    elif seconds < 604800:  # less than a week
        days = int(seconds // 86400)
        return f'{convert_to_persian_words(days)} روز پیش'
    elif seconds < 2592000:  # less than a month
        weeks = int(seconds // 604800)
        return f'{convert_to_persian_words(weeks)} هفته پیش'
    elif seconds < 31536000:  # less than a year
        months = int(seconds // 2592000)
        return f'{convert_to_persian_words(months)} ماه پیش'
    else:
        years = int(seconds // 31536000)
        return f'{convert_to_persian_words(years)} سال پیش'

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
