from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

# Create your views here.

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        # Check if password matches
        if password == password2:
            #check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is already taken')
                return redirect('register')
            else :
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is already taken')
                    return redirect('register')
                else: 
                    #CREATE USER
                    user = User.objects.create_user(username = username, password = password, first_name = first_name,
                    last_name = last_name, email = email)

                    # #LOGIN AFTER REGISTER
                    # auth.login(request, user)
                    # messages.success(request, 'You are logged in')
                    # return redirect('index')

                    # Register the user and redirect to the user login
                    user.save();
                    messages.success(request, 'You are now register')
                    return redirect('login')

        else:
            messages.error(request, 'Password do not match')
            return redirect('register')    
        return
    else:
        return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        #login USER
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Username or Password not valid')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id = request.user.id)
    res = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', res)
