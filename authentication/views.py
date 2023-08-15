from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urisafe_base64_encode
from django.utils.encoding import force_bytes,force_text
from . tokens import generate_token
from django.core.mail import EmailMessage,send_mail


from signin_page import settings

# Create your views here.
def home(request):
    #return HttpResponse("Hello I am Working on it")
    return render(request,"authentication/index.html")

def signup(request):

    if request.method =="POST":
        #username = request.POST.get('username')
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']


        if User.objects.filter(username=username):
            messages.error(request,"Username already exist! Please try some other username")
            return redirect('home')
        
        if User.objects.filter(email=email):
            messages.error(request,'Email is Already Exist!')
            return redirect('home')
        if len(username)>10:
            messages.error(request,'Username must be below 10 character')

        if pass1 != pass2:
            messages.error(request,"Passwords didn't match!")

        if not username.isalnum():
            messages.error(request,'Username must be alpha-Numeric!')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request,"Your Account has been created Sucessfully. we have send you a confirmation email. Please verify it by click the link attached in mail")



        #welcome email

        subject ="Welcome to our page!!"
        message ="hello" + myuser.first_name + "!!\n" + "welcome to page!! \n Thank you for visiting \n please conform your email address\
            \n \n Thank You" 
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list, fail_silently=True)
        return redirect('signin')

        #email conformation
        current_site = get_current_site(request)
        email_subject = "Confirm your email @page"
        message2 = render_to_string('email_confirmation.html'),{
            'name':myuser.first_name,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token':generate_token.make_token(myuser)
        }
        email = EmailMessage(
            email_subject,
            message2,
            setting.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()





    #return HttpResponse("Hello Ur in signup page")
    return render(request,"authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username = username, password = pass1)
        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/index.html", {'fname':fname})
        else:
            messages.error(request, "Bad login Credentials")
            return redirect('home')
    #return HttpResponse("Hello Ur in signin page")
    return render(request,"authentication/signin.html")

def signout(request):
    #return HttpResponse("Hello Ur in signout page")
    logout(request)
    messages.success(request,"Logged Out Sucessfully")
    return redirect('home')
