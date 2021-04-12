from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import NewUser
# Create your views here.
def login(request):
    if request.method == 'POST':
        email =  request.POST['email']
        password =  request.POST['pass']
        user = auth.authenticate(email = email,password = password)
        print(user)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/login/')
    else:
        return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username =  request.POST['username']
        ign =  request.POST['ign']
        email =  request.POST['email']
        pass1 =  request.POST['pass1']
        pass2 =  request.POST['pass2']
        phone =  request.POST['phone']
        if 'is_organizer"' in request.POST:
            is_organizer = request.POST['is_organizer']
        else:
            is_organizer = False
        print('ok1')
        if pass1 == pass2:
            if NewUser.objects.filter(username = username).exists():
                messages.info(request,'Username Taken')
                return redirect('/signup/')
            elif NewUser.objects.filter(email = email).exists():
                messages.info(request,'Email Taken')
                return redirect('/signup/')
            else:
        
                user = NewUser.objects.create_user(email=email,username = username,ign=ign,phone=phone,password=pass1,is_organizer=True)
                
                user.save()
                print('ok')
                return redirect('/login/')
        else:
            messages.info(request,'Password does not match')
            return redirect('/signup/')

    else:
        return render(request,'signup.html')


def logout(request):
    auth.logout(request)
    return redirect('/')