from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest
from .models import User

def index(request):
  return render(request, 'usermgmt/index.html')

def register(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    # SECURITY FLAW: Identification and Authentication Failures
    # - no strong password validation, or any validation at all
    # - storing passwords in plaintext
    #
    # FIX: use Django's built-in authentication utilities
    # - use Django's User model which includes password encryption
    # - use Django's default password validation for enforcing strong passwords
    #   and for even more improvement, add couple more custom validations
    new_user = User(username=username, password=password)
    new_user.save()
    return redirect('polls:index')
  
  else:
    return render(request, 'usermgmt/register.html')

def login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    # SECURITY FLAW: Injection
    # - accepting non-sanitized inputs introduces injection vulnerability
    # 
    # FIX: Use parameterized queries or Django's own User Model
    query = "SELECT * FROM usermgmt_user WHERE username = '%s'" %username
    user = User.objects.raw(query)[0]
    
    # SECURITY FLAW: Identification and Authentication Failures
    # - weak authentication method.
    # 
    # FIX: use Django's built-in authentication utilities
    if user.password == password:
      return redirect('polls:index')

    else:
      return HttpResponseBadRequest('invalid password')

  else:
    return render(request, 'usermgmt/login.html')

# FIXED VERSION (replace the lines above with these):
# from django.shortcuts import redirect, render
# from django.http import HttpResponseBadRequest
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate, login as auth_login
# from django.contrib.auth.password_validation import validate_password

# def index(request):
#   return render(request, 'usermgmt/index.html')

# def register(request):
#   if request.method == 'POST':
#     username = request.POST['username']
#     password = request.POST['password']
#     validate_password(password)
#     user = User.objects.create_user(username, None, password)
#     user.save()
#     auth_login(request, user)
#     return redirect('polls:index')
  
#   else:
#     return render(request, 'usermgmt/register.html')

# def login(request):
#   if request.method == 'POST':
#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#       auth_login(request, user)
#       return redirect('polls:index')

#     else:
#       return HttpResponseBadRequest('invalid password')

#   else:
#     return render(request, 'usermgmt/login.html')

