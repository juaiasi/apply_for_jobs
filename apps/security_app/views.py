from datetime import timedelta, date
from .validation.validation import validated_fields
from .validation.authorization import authorized_to_display_pw
from django.shortcuts import render, get_object_or_404, redirect
from security_app.models import Sharer 
from django.contrib.auth.models import User
from shortuuid import ShortUUID
from django.contrib import auth, messages

def dashboard(request):
    if request.user.is_superuser and request.user.is_authenticated:
        sharer_list = Sharer.objects.all()
        data = {
            'sharers':sharer_list
        }
        return render(request,'sharing/dashboard.html',data)
    elif request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request,"Você tentou acessar uma área restrita")
        return redirect('logged')
    else:
        messages.warning(request,"Área restrita")
        return redirect('login')

def create_sharer(request):
    if request.user.is_superuser and request.user.is_authenticated:
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

            if not validated_fields(fields,request):
                return redirect('create_sharer')

            if Sharer.objects.filter(user=user).exists():
                Sharer.objects.filter(user=user).update(user=user,
                                                        code=fields['code'],
                                                        limit_visits=fields['limit_visits'],
                                                        limit_datetime=fields['limit_datetime'],
                                                        password=fields['password'],
                                                        public=True)
            else:
            # Criar sharer
                sharer = Sharer.objects.create(user=user,
                                                code=fields['code'],
                                                limit_visits=fields['limit_visits'],
                                                limit_datetime=fields['limit_datetime'],
                                                password=fields['password'])
                sharer.save()

            # Atualizar senha do usuário

            user.set_password(fields['password'])
            user.save()

            return redirect('display_link',user=fields['user'].id)
        else:
            users = User.objects.filter(is_superuser=False)
            data = {
                'users':users,
                'date': str(date.today() + timedelta(days = 7))
            }
            return render(request, 'sharing/create_sharer.html', data)
    elif request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request,"Você tentou acessar uma área restrita")
        return redirect('logged')
    messages.warning(request,"Área restrita.")
    return redirect('login')

def display_link(request,user):
    if request.user.is_superuser and request.user.is_authenticated:
        sharer = get_object_or_404(Sharer, user=user)
        data ={
            'sharer':sharer
        }
        return render(request,'sharing/display_link.html',data)
    elif request.user.is_authenticated and not request.user.is_superuser:
        messages.warning(request,"Você tentou acessar uma área restrita")
        return redirect('logged')
    messages.warning(request,"Área restrita.")
    return redirect('login')

def sharer(request,code):
    sharer = get_object_or_404(Sharer, code=code)
    if authorized_to_display_pw(sharer):
        limit_visits = sharer.limit_visits - 1
        Sharer.objects.filter(code=code).update(limit_visits=limit_visits)
        data ={
            'sharer':sharer
        }
        return render(request, 'sharing/sharer.html', data)
    else:
        messages.info(request,'A senha não está mais disponível para visualização. Caso precise recuperá-la, peça ao adminstrador para gerar um novo link.')
        Sharer.objects.filter(code=code).update(public=False,password="")
        return render(request, 'sharing/sharer.html')

def login(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if password == "" or password == "":
            messages.error(request,"Nenhum campo pode estar em branco.")
            return redirect('login')
        
        user_exists = User.objects.filter(username=username).exists()
        authenticated = auth.authenticate(request,username=username,password=password)
        if user_exists and authenticated is not None:
            user = User.objects.filter(username=username).get()
            if user.is_superuser:
                auth.login(request,authenticated)
                return redirect('dashboard')
            auth.login(request,authenticated)
            return redirect('logged')
        messages.error(request,'Usuário não existe ou os dados estão incorretos')
    
    if request.user.is_authenticated:
        auth.logout(request)
        messages.warning(request,'Você foi desconectado.')
    return render(request, 'user/login.html')

def logged(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return redirect('login')
        return render(request, 'user/logged.html')
    else:
        messages.warning(request,'Você não está logado.')
        return redirect('login')

# -----------------------------------------------
# Complementary functions

def generate_code():
    while True:
        code = ShortUUID(alphabet="0123456789").random(length=5)
        try:
            Sharer.objects.get(code=code)
        except:
            break
    return code


