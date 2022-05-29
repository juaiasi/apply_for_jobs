from datetime import datetime, timedelta, date
from .validation.validation import fields_validated
from .validation.authorization import authorized_to_display_pw
from django.shortcuts import render, get_object_or_404, redirect
from security_app.models import Sharer 
from django.contrib.auth.models import User
from shortuuid import ShortUUID
from django.contrib import auth, messages


def dashboard(request):
    """View: Dashboard with created links. Access restricted to superuser."""
    is_authenticated = request.user.is_authenticated
    is_superuser = request.user.is_superuser

    # If user is authenticated and is superuser, render dashboard
    if is_authenticated and is_superuser:
        sharer_list = Sharer.objects.all()

        # If sharer has expired, set public to false and password is deleted
        for sharer in sharer_list:
            if not authorized_to_display_pw(sharer):
                Sharer.objects.filter(code=sharer.code).update(public=False,password="")

        data = {
            'sharers':sharer_list
        }

        return render(request,'sharing/dashboard.html',data)

    # If user is authenticated but is not a superuser, go back to "Logged" page with a warning message
    elif is_authenticated and not is_superuser:
        messages.warning(request, "Você tentou acessar uma área restrita")
        return redirect('logged')
    
    # If user is not authenticated, redirect to login page
    messages.warning(request,"Área restrita")
    return redirect('login')


def create_sharer(request):
    """View: Page for creating sharer link. Access restricted to superuser."""
    is_authenticated = request.user.is_authenticated
    is_superuser = request.user.is_superuser

    # If user is authenticated and is superuser... 
    if is_superuser and is_authenticated:
        
        # If created...
        if request.method == 'POST':
            user = get_object_or_404(User, username=request.POST['username'])
            fields = {
                'username': request.POST['username'],
                'password': request.POST['password'],
                'user': user,
                'code': generate_code(),
                'limit_visits': request.POST['limit_visits'],
                'limit_datetime': request.POST['limit_datetime']
            }

            # Validate fields
            if not fields_validated(fields,request):
                return redirect('create_sharer')
            
            # Check if sharer alredy exists
            if Sharer.objects.filter(user=user).exists():
                Sharer.objects.filter(user=user).update(user=user,
                                                        code=fields['code'],
                                                        limit_visits=fields['limit_visits'],
                                                        limit_datetime=fields['limit_datetime'],
                                                        password=fields['password'],
                                                        public=True)
            # Else, create sharer
            else:
                sharer = Sharer.objects.create(user=user,
                                                code=fields['code'],
                                                limit_visits=fields['limit_visits'],
                                                limit_datetime=fields['limit_datetime'],
                                                password=fields['password'])
                sharer.save()

            # Update user password
            user.set_password(fields['password'])
            user.save()

            # Show to superuser the link do share
            return redirect('display_link',user=fields['user'].id)
        
        # Get: render "Create Sharer" page
        else:
            users = User.objects.filter(is_superuser=False)
            data = {
                'users':users,
                'date': str(date.today() + timedelta(days = 7))
            }

            return render(request, 'sharing/create_sharer.html', data)
    
    # If user is authenticated but is not a superuser, go back to "Logged" page with a warning message
    elif is_authenticated and not is_superuser:
        messages.warning(request,"Você tentou acessar uma área restrita")
        return redirect('logged')
    
    # If user is not authenticated, redirect to login page
    messages.warning(request,"Área restrita.")
    return redirect('login')


def display_link(request,user):
    """Views: Link display with other informations for superuser visualization e sharing"""
    is_authenticated = request.user.is_authenticated
    is_superuser = request.user.is_superuser

    # If user is authenticated and is superuser, render link display page
    if is_superuser and is_authenticated:
        sharer = get_object_or_404(Sharer, user=user)

        # If sharer has expired, set public to false and password is deleted
        if not authorized_to_display_pw(sharer):
            Sharer.objects.filter(code=sharer.code).update(public=False,password="")

        data ={
            'sharer':sharer
        }

        return render(request,'sharing/display_link.html',data)

    # If user is authenticated but is not a superuser, go back to "Logged" page with a warning message
    elif is_authenticated and not is_superuser:
        messages.warning(request,"Você tentou acessar uma área restrita")
        return redirect('logged')
    
    # If user is not authenticated, redirect to login page
    messages.warning(request,"Área restrita.")
    return redirect('login')


def sharer(request,code):
    """View: Password sharer, that contains expiration information. It controls when the password sharing expires"""
    sharer = get_object_or_404(Sharer, code=code)

    # If sharer has not expired, render the page and update the number of views available
    if authorized_to_display_pw(sharer):
        limit_visits = sharer.limit_visits - 1
        Sharer.objects.filter(code=code).update(limit_visits=limit_visits)
        data ={
            'sharer':sharer
        }
        return render(request, 'sharing/sharer.html', data)
    
    # Else, password is deleted of database and show up a info message
    else:
        messages.info(request,'A senha não está mais disponível para visualização. Caso precise recuperá-la, peça ao adminstrador para gerar um novo link.')
        Sharer.objects.filter(code=code).update(public=False,password="")
        return render(request, 'sharing/sharer.html')


def login(request):
    """View: Login"""

    # If login button was clicked...
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # If the fields are blank, reload login page with error message
        if password == "" or password == "":
            messages.error(request,"Nenhum campo pode estar em branco.")
            return redirect('login')
        
        user_exists = User.objects.filter(username=username).exists()
        authenticated = auth.authenticate(request,username=username,password=password)

        # If user exists and is authenticated
        if user_exists and authenticated is not None:
            user = User.objects.filter(username=username).get()
            if user.is_superuser:
                auth.login(request,authenticated)
                return redirect('dashboard')
            auth.login(request,authenticated)
            return redirect('logged')

        # Else, shows up an error message
        messages.error(request,'Usuário não existe ou os dados estão incorretos')
    
    # Logout if user is logged in, with warning message
    if request.user.is_authenticated:
        auth.logout(request)
        messages.warning(request,'Você foi desconectado.')
    
    # Else, just render the page
    return render(request, 'user/login.html')

def logged(request):
    """Views: 'Logged in' page, just for testing"""

    # If is authenticated...
    if request.user.is_authenticated:

        # Logout if button "Sair" is clicked
        if request.method == 'POST':
            return redirect('login')
        
        # Else, just render the page 
        return render(request, 'user/logged.html')
    
    # Reload login page and shows up a warning message if user is not authenticated
    messages.warning(request,'Você não está logado.')
    return redirect('login')

# -----------------------------------------------
# Complementary functions

def generate_code(len=16):
    """Function to generate code, that will be used to construct the url of sharer.
    Parameter: 'len' = length of code"""

    while True:
        code = ShortUUID(alphabet="0123456789").random(length=len)
        try:
            # Check if code already exists in the database
            Sharer.objects.get(code=code)
        except:
            break
        
    return code


