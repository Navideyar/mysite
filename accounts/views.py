from django.shortcuts import render , redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm , UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import re

@ensure_csrf_cookie
def login_view(request):
    # اگر کاربر قبلاً وارد شده باشد، به صفحه اصلی هدایت می‌شود
    if request.user.is_authenticated:
        # اگر کاربر مدیر است، نیازی به استفاده از این صفحه ندارد
        # مدیران باید مستقیما از صفحه ادمین استفاده کنند
        return redirect('/')
        
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
             
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # اگر کاربر مدیر باشد، به این صفحه دسترسی نداشته باشد
                if user.is_staff:
                    # به صفحه اصلی برمی‌گردیم و پیام می‌دهیم که لطفا از صفحه ادمین استفاده کنید
                    return render(request, 'accounts/login.html', {'error': 'لطفا به عنوان مدیر از صفحه ادمین وارد شوید'})
                
                login(request, user)
                messages.success(request, f'خوش آمدید {username}!')
                
                # هدایت به صفحه اصلی یا صفحه قبلی
                next_url = request.GET.get('next', '/')
                return redirect(next_url) 
            else:
                # اگر اطلاعات ورود نادرست باشد، پیام خطا نمایش داده شود
                return render(request, 'accounts/login.html', {'error': 'نام کاربری یا رمز عبور اشتباه است', 'form': form})
        else:
            # اگر فرم معتبر نباشد، خطاهای فرم را نمایش بده
            return render(request, 'accounts/login.html', {'error': 'اطلاعات وارد شده معتبر نیست', 'form': form})
            
    form = AuthenticationForm()
    context = {
        'form': form
    }
    # اگر درخواست GET باشد، صفحه ورود را نمایش بده
    return render(request, 'accounts/login.html', context)

def admin_redirect_view(request):
    # این تابع دیگر مورد نیاز نیست، اما می‌توانیم آن را نگه داریم
    # برای احتیاط و اطمینان از سازگاری با کدهای قبلی
    return redirect('/admin/')

@ensure_csrf_cookie
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/')
        
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')
        
        # بررسی وجود تمام فیلدها
        if not (username and email and password1 and password2):
            return render(request, 'accounts/signup.html', {'error': 'لطفاً همه فیلدها را پر کنید'})
            
        # اعتبارسنجی نام کاربری
        if not re.match(r'^[\w.@+-]+$', username):
            return render(request, 'accounts/signup.html', {'error': 'نام کاربری فقط می‌تواند شامل حروف، اعداد و علائم @ . + - _ باشد'})
            
        # اعتبارسنجی ایمیل
        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'accounts/signup.html', {'error': 'لطفاً یک آدرس ایمیل معتبر وارد کنید'})
            
        # بررسی قوی بودن رمز عبور
        if len(password1) < 8:
            return render(request, 'accounts/signup.html', {'error': 'رمز عبور باید حداقل ۸ کاراکتر باشد'})
            
        # بررسی تطابق رمزهای عبور
        if password1 != password2:
            return render(request, 'accounts/signup.html', {'error': 'رمزهای عبور مطابقت ندارند'})
            
        # بررسی تکراری نبودن نام کاربری
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/signup.html', {'error': 'این نام کاربری قبلاً استفاده شده است'})
            
        # بررسی تکراری نبودن ایمیل
        if User.objects.filter(email=email).exists():
            return render(request, 'accounts/signup.html', {'error': 'این ایمیل قبلاً استفاده شده است'})
            
        try:
            # ایجاد کاربر جدید
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            
            # در یک سیستم واقعی، اینجا ایمیل تأیید ارسال می‌شود
            # اما فعلاً فقط شبیه‌سازی می‌کنیم
            
            # ورود خودکار کاربر
            login(request, user)
            messages.success(request, f'ثبت نام با موفقیت انجام شد! خوش آمدید {username}')
            return redirect('/')
        except Exception as e:
            return render(request, 'accounts/signup.html', {'error': f'خطا در ثبت نام: {str(e)}'})
        
    return render(request, 'accounts/signup.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'با موفقیت از حساب کاربری خارج شدید.')
    return redirect('/')
